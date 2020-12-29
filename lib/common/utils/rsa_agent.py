# coding:utf-8
# https://stuvel.eu/python-rsa-doc/usage.html#generating-keys
import rsa
import json
from rsa import PublicKey, PrivateKey


class RsaCrypto:
    PUBLIC_KEY_START = "=" * 15 + "PUBLIC-KEY" + "=" * 15
    PRIMARY_KEY_START = "=" * 15 + "PRIMARY-KEY" + "=" * 15
    SPLIT_CODE = "(^&QA*%=="

    @staticmethod
    def newkeys(b=1024):
        return rsa.newkeys(b)

    @staticmethod
    def encoded_text(s, public_key):
        return rsa.encrypt(s.encode('utf-8'), public_key)

    @staticmethod
    def decoded_text(s_encoded, primary_key):
        return rsa.decrypt(s_encoded, primary_key).decode('utf-8')

    @staticmethod
    def check_keys(public_key, primary_key, text=''):
        encoded_text = rsa.encrypt(text.encode('utf-8'), public_key)
        decoded_text = rsa.decrypt(encoded_text, primary_key).decode('utf-8')
        if str(decoded_text) == str(text):
            return True
        return False

    @staticmethod
    def encode_json(obj, public_key):
        """
        使用rsa 加密Json对象
        :param obj: json对象 dict
        :param public_key: 公钥
        :return:
        """
        return RsaCrypto.encoded_text(s=json.dumps(obj), public_key=public_key)

    @staticmethod
    def decode_json(b_encoded, primary_key):
        """
        传进去加密的字符串和加密的密钥
        :param b_encoded: 加密后的二进制流
        :param primary_key: 解密的私钥
        :return:
        """
        return json.loads(RsaCrypto.decoded_text(s_encoded=b_encoded, primary_key=primary_key))

    @staticmethod
    def write_bytes_to_file(_bytes, file_path):
        with open(file_path, "wb") as f:
            f.write(_bytes)
            f.close()

    @staticmethod
    def write_str_to_file(s, file_path):
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(s)
            f.close()

    @staticmethod
    def loads_strs_from_file(file_path):
        with open(file_path, "r", encoding='utf-8') as f:
            string = f.read()
            f.close()
        return string

    @staticmethod
    def get_publickey_txt(public_key):
        n, e = public_key.n, public_key.e
        return RsaCrypto.PUBLIC_KEY_START + "\n" + RsaCrypto.SPLIT_CODE.join([str(n), str(e)])

    @staticmethod
    def get_privatekey_txt(pri_key):
        """
        传递进来Primary_key对象，生成我们需要的文本key
        :param pri_key:
        :return:
        """
        n, e, d, p, q = pri_key.n, pri_key.e, pri_key.d, pri_key.p, pri_key.q
        return RsaCrypto.PRIMARY_KEY_START + "\n" + RsaCrypto.SPLIT_CODE.join([str(x) for x in [n, e, d, p, q]])

    @staticmethod
    def write_strkey_to_file(s_key, file_path):
        """
        将字符串类型的s_key写入到文件路径 file_path中
        :param s_key:
        :param file_path:
        :return:
        """
        RsaCrypto.write_str_to_file(s_key, file_path)

    @staticmethod
    def loads_publickey_from_file(file_path):
        """
        从文件中加载生成 pub_key 对象
        :param file_path:
        :return:
        """
        n, e = RsaCrypto.loads_strs_from_file(file_path).split("\n")[1].split(RsaCrypto.SPLIT_CODE)
        return PublicKey(int(n), int(e))

    @staticmethod
    def loads_privatekey_from_file(file_path):
        n, e, d, p, q = RsaCrypto.loads_strs_from_file(file_path).split("\n")[1].split(RsaCrypto.SPLIT_CODE)
        return PrivateKey(*[int(x) for x in [n, e, d, p, q]])

    @staticmethod
    def from_key_str_get_obj(s_key):
        # 先把 \n 去掉再获取
        args = [int(x) for x in s_key.split("\n")[1].split(RsaCrypto.SPLIT_CODE)]
        if len(args) == 2:
            return PublicKey(*args)
        if len(args) == 5:
            return PrivateKey(*args)
        raise EOFError('长度异常')


def test_write_keys():
    public_key_file = "d://rsa_keys//public.key"
    primary_key_file = "d://rsa_keys//primary.key"

    public_key, primary_key = RsaCrypto.newkeys(2048)
    RsaCrypto.write_strkey_to_file(RsaCrypto.get_publickey_txt(public_key), public_key_file)
    RsaCrypto.write_strkey_to_file(RsaCrypto.get_privatekey_txt(primary_key), primary_key_file)


def test_loads_keys():
    public_key_file = "d://rsa_keys//public.key"
    primary_key_file = "d://rsa_keys//primary.key"

    public_key = RsaCrypto.loads_publickey_from_file(public_key_file)
    primary_key = RsaCrypto.loads_privatekey_from_file(primary_key_file)
    status = RsaCrypto.check_keys(public_key, primary_key)

    print(status)


if __name__ == '__main__':
    test_write_keys()
    print('开始检查')
    test_loads_keys()