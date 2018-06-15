# hbase 数据表解析

hbase(main):017:0> scan 'test'

	ROW                                             COLUMN+CELL
	 r1                                             column=cf:age, timestamp=1528940729285, value=18
	 r1                                             column=cf:name, timestamp=1528940763048, value=abc
	 r2                                             column=cf:name, timestamp=1528940781541, value=hello

hbase(main):016:0> desc 'test'

    Table test is ENABLED                                                                                                                 
    test                                                                                                                                  
    COLUMN FAMILIES DESCRIPTION                                                                                                           
    {NAME => 'cf', BLOOMFILTER => 'ROW', VERSIONS => '1', IN_MEMORY => 'false', KEEP_DELETED_CELLS => 'FALSE', DATA_BLOCK_ENCODING => 'NON
    E', TTL => 'FOREVER', COMPRESSION => 'NONE', MIN_VERSIONS => '0', BLOCKCACHE => 'true', BLOCKSIZE => '65536', REPLICATION_SCOPE => '0'
    }  

    NAME        列族名
    VERSIONS    时间版本
    REPLICATION_SCOPE 复本
    COMPRESSION 压缩

压缩算法

    Algorithm   remaining   Encoding    Decoding
    算法        压缩率      编码        解码
    GZip        13.4%       21MB/s      118MB/s
    LZO         20.5%       135MB/s     410MB/s
    Snappy      22.2%       172MB/s     409MB/s     推荐


