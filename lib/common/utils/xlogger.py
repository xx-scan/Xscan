#!/usr/bin/python3.6

import os
import sys
import socket
import datetime

# Only imported for the syslog.LOG_INFO and syslog.LOG_USER constants.
import syslog


# Appends a newline in all cases.
def _log_stderr(message):
    if message:
        sys.stderr.write(message)
    sys.stderr.write('\n')
    sys.stderr.flush()

# XSyslog: a syslog wrapper class.
#
# This module allows the facility (such as LOG_USER), the
# severity (such as LOG_INFO), and other syslog parameters
# to be set on a message-by-message basis via one, single
# syslog connection.
#
# Usage:
#
#   slog = XSyslog([server=server], [port=port], [proto=proto],
#                  [clientname=clientname], [maxlen=maxlen])
#
# This allows three  cases:
# (1) Connect to syslog via UDP to a host and port:
#     Specify host, port, and proto='UDP'.
# (2) Connect to syslog via TCP to a host and port:
#     Specify host, port, and proto='TCP'.
# (3) Connect to syslog via a socket file such as /dev/log.
#     Specify proto=filename (e.g., proto='/dev/log').
#     In this case, host and port are ignored.
#
# clientname is an optional field for the syslog message.
# maxlen is the maximum message length.
#
# Once the XSyslog object is created, the message can be sent as follows:
#
#   slog = XSyslog([... parameters ...])
#   slog.log(message, [facility=facility], [severity=severity],
#                     [timestamp=timestamp], [hostame=hostname],
#                     [program=program], [pid=pid])
#     facility  defaults to LOG_USER
#     severity  defaults to LOG_INFO
#     timestamp defaults to now
#     hostname  if None, use clientname if it exists; if '', no hostname.
#     program   defaults to "logger"
#     pid       defaults to os.getpid()


class XSyslog(object):

    def __init__(self, server=None, port=None, proto='udp', clientname=None, maxlen=1024):
        self.server       = server
        self.port         = port
        self.proto        = socket.SOCK_DGRAM
        self.clientname   = clientname
        self.maxlen       = maxlen
        self._protoname   = ''
        self._socket      = None
        self._sockfile    = None
        self._connectargs = ()
        self._me          = os.path.splitext(self.__class__.__name__)[1][1:]

        if proto:
            if proto.lower() == 'udp':
                self._protoname  = proto.lower()
                self.proto       = socket.SOCK_DGRAM
                self._socketargs = (self.server, self.port, socket.AF_UNSPEC, self.proto)
            elif proto.lower() == 'tcp':
                self._protoname  = proto.lower()
                self.proto       = socket.SOCK_STREAM
                self._socketargs = (self.server, self.port, socket.AF_UNSPEC, self.proto)
            elif len(proto) > 0:
                self._sockfile   = proto
                self._protoname  = self._sockfile
                self.proto       = socket.SOCK_DGRAM
                self._socketargs = (socket.AF_UNIX, self.proto)

        badargs = False
        if self._sockfile:
            pass
        elif self.server and self.port:
            pass
        else:
            badargs = True
        if not self.proto:
            badargs = True
        if badargs:
            raise ValueError("'proto' must be 'udp' or 'tcp' with 'server' and 'port', or else a socket filename like '/dev/log'")

        if not self.clientname:
            try:
                self.clientname = socket.getfqdn()
                if not self.clientname:
                    self.clientname = socket.gethostname()
            except:
                self.clientname = None

    def _connect(self):
        if self._socket is None:
            if self._sockfile:
                self._socket = socket.socket(*self._socketargs)
                if not self._socket:
                    _log_stderr(':::::::: {}: unable to open socket file {}'.format(self._me, self._sockfile))
                    return False
                try:
                    self._socket.connect(self._sockfile)
                    return True
                except socket.timeout as e:
                    _log_stderr(':::::::: {}: sockfile timeout e={}'.format(self._me, e))
                    # Force-close the socket and its contained fd, to avoid fd leaks.
                    self.close()
                except socket.error as e:
                    _log_stderr(':::::::: {}: sockfile error f={}, e={}'.format(self._me, self._sockfile, e))
                    # Force-close the socket and its contained fd, to avoid fd leaks.
                    self.close()
                except Exception as e:
                    # Any other exception which might occur ...
                    _log_stderr(':::::::: {}: sockfile exception f={}, e={}'.format(self._me, self._sockfile, e))
                    # Force-close the socket and its contained fd, to avoid fd leaks.
                    self.close()
                return False
            else:
                addrinfo = socket.getaddrinfo(*self._socketargs)
                if addrinfo is None:
                    return False
                # Check each socket family member until we find one we can connect to.
                for (addr_fam, sock_kind, proto, ca_name, sock_addr) in addrinfo:
                    self._socket = socket.socket(addr_fam, self.proto)
                    if not self._socket:
                        _log_stderr(':::::::: {}: unable to get a {} socket'.format(self._me, self._protoname))
                        return False
                    try:
                        self._socket.connect(sock_addr)
                        return True
                    except socket.timeout as e:
                        _log_stderr(':::::::: {}: {} timeout e={}'.format(self.me, self._protoname, e))
                        # Force-close the socket and its contained fd, to avoid fd leaks.
                        self.close()
                        continue
                    except socket.error as e:
                        _log_stderr(':::::::: {}: {} error e={}'.format(self._me, self._protoname, e))
                        # Force-close the socket and its contained fd, to avoid fd leaks.
                        self.close()
                        continue
                    except Exception as e:
                        # Any other exception which might occur ...
                        _log_stderr(':::::::: {}: {} exception e={}'.format(self._me, self._protoname, e))
                        # Force-close the socket and its contained fd, to avoid fd leaks.
                        self.close()
                        continue
                # Force-close the socket and its contained fd, to avoid fd leaks.
                self.close()
                return False
        else:
            return True

    def close(self):
        try:
            self._socket.close()
        except:
            pass
        self._socket = None

    def log(self, message, facility=None, severity=None, timestamp=None, hostname=None, program=None, pid=None):

        if message is None:
            return

        if not facility:
            facility = syslog.LOG_USER

        if not severity:
            severity = syslog.LOG_INFO

        pri = facility + severity

        data = '<{}>'.format(pri)

        if timestamp:
            t = timestamp
        else:
            t = datetime.datetime.now()
        data = '{}{}'.format(data, t.strftime('%Y-%m-%dT%H:%M:%S.%f'))

        if hostname is None:
            if self.clientname:
                data = '{} {}'.format(data, self.clientname)
        elif not hostname:
            # For hostname == '', leave out the hostname, altogether.
            pass
        else:
            data = '{} {}'.format(data, hostname)

        if program:
            data = '{} {}'.format(data, program)
        else:
            data = '{} logger'.format(data)

        if not pid:
            pid = os.getpid()

        data = '{}[{}]: {}'.format(data, pid, message).encode('ascii', 'ignore')

        if not self._socket:
            self._connect()

        if not self._socket:
            raise Exception('{}: unable to connect to {} syslog via {}'.format(self._me, self._protoname, self._socketargs))
        try:
            if self.maxlen:
                self._socket.sendall(data[:self.maxlen])
            else:
                self._socket.sendall(data)
        except IOError as e:
            _log_stderr(':::::::: {}: {} syslog io error {} via {}'.format(self._me, self._protoname, e, self._socketargs))
            self.close()
            raise
        except Exception as e:
            # Any other exception which might occur ...
            _log_stderr(':::::::: {}: {} syslog exception {} via {}'.format(self._me, self._protoname, e, self._socketargs))
            self.close()
            raise