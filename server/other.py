from flask import Response

def anticheat():

    # XML内容
    xml_content = '''
    <?xml version="1" encoding="utf-8"?>
    <config>
        <DEFAULT ct="00000000000000000000000000000000" probability="100" flag="1">
            <file type=3 local="files/tss_ano.dat" name="tss_ano.dat" hash_type=1 probability="100" scale="1">
                <A hash="5D189833"/>
                <B hash="49AAD6D2"/>
            </file>
            <file type=3 local="files/comm.dat" name="comm.dat" hash_type=1 probability="100" scale="1">
                <A hash="07813426"/>
                <B hash="6B5F1E74"/>
            </file>
            <file type=3 local="files/tp2cfg.dat" name="tp2cfg.dat" hash_type=1 probability="100" scale="1">
                <A hash="A93010EC"/>
                <B hash="4307C862"/>
            </file>
        </DEFAULT>
    </config>
    '''

    # 创建响应对象，设置内容类型为application/xml
    response = Response(xml_content, content_type='application/xml')
    
    # 添加HTTP头信息
    response.headers['Content-Length'] = str(len(xml_content))
    response.headers['Accept-Ranges'] = 'bytes'
    response.headers['ETag'] = '"26c70887ede81610f1b93be458c472c5"'
    response.headers['Last-Modified'] = 'Thu, 08 Dec 2022 03:06:00 GMT'
    response.headers['Server'] = 'tencent-cos'
    response.headers['x-cos-hash-crc64ecma'] = '13798635531983689788'
    response.headers['x-cos-replication-status'] = 'Replica'
    response.headers['x-cos-request-id'] = 'NjQyNmQwMWFfNTdjZDExMGJfMTRhMTBfNzliYmMzNQ=='
    response.headers['x-cos-version-id'] = 'MTg0NDUwNzM2MDQ5NDkzMDUwNjA'
    response.headers['Age'] = '1'
    response.headers['X-Via'] = '1.1 houdianxin55:11 (Cdn Cache Server V2.0), 1.1 PS-CAN-01Pk269:3 (Cdn Cache Server V2.0)'
    response.headers['X-Ws-Request-Id'] = '669c72f7_PS-CAN-01Pk269_32160-7647'
    response.headers['Cache-Control'] = 'no-cache,no-store'

    return response

def event():

    return {
        "code": 200,
        "msg": "OK",
    }
    
def batch_event():

    {
    "code": 200,
    "msg": "OK",
    "next": 180
    }

def beat():

    # 来自bi-track.hypergryph.com:443 101.132.113.1:443

    {
    "code": 200,
    "msg": "ok",
    "next": 257
    }

def deviceprofile():

    return {}