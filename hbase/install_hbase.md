# start hbase

    ./bin/start-hbase.sh

Connect to HBase.

    Connect to your running instance of HBase using the hbase shell command, located in the bin/ directory of your HBase install. In this example, some usage and version information that is printed when you start HBase Shell has been omitted. The HBase Shell prompt ends with a > character.

    $ ./bin/hbase shell
    hbase(main):001:0>

    Display HBase Shell Help Text.

    Type help and press Enter, to display some basic usage information for HBase Shell, as well as several example commands. Notice that table names, rows, columns all must be enclosed in quote characters.

Create a table.

    Use the create command to create a new table. You must specify the table name and the ColumnFamily name.

    hbase(main):001:0> create 'test', 'cf'
    0 row(s) in 0.4170 seconds

    => Hbase::Table - test

    List Information About your Table

    Use the list command to confirm your table exists

    hbase(main):002:0> list 'test'
    TABLE
    test
    1 row(s) in 0.0180 seconds

    => ["test"]

    Now use the describe command to see details, including configuration defaults

    hbase(main):003:0> describe 'test'
    Table test is ENABLED
    test
    COLUMN FAMILIES DESCRIPTION
    {NAME => 'cf', VERSIONS => '1', EVICT_BLOCKS_ON_CLOSE => 'false', NEW_VERSION_BEHAVIOR => 'false', KEEP_DELETED_CELLS => 'FALSE', CACHE_DATA_ON_WRITE =>
    'false', DATA_BLOCK_ENCODING => 'NONE', TTL => 'FOREVER', MIN_VERSIONS => '0', REPLICATION_SCOPE => '0', BLOOMFILTER => 'ROW', CACHE_INDEX_ON_WRITE => 'f
    alse', IN_MEMORY => 'false', CACHE_BLOOMS_ON_WRITE => 'false', PREFETCH_BLOCKS_ON_OPEN => 'false', COMPRESSION => 'NONE', BLOCKCACHE => 'true', BLOCKSIZE
     => '65536'}
    1 row(s)
    Took 0.9998 seconds

Put data into your table.

    To put data into your table, use the put command.

    hbase(main):003:0> put 'test', 'row1', 'cf:a', 'value1'
    0 row(s) in 0.0850 seconds

    hbase(main):004:0> put 'test', 'row2', 'cf:b', 'value2'
    0 row(s) in 0.0110 seconds

    hbase(main):005:0> put 'test', 'row3', 'cf:c', 'value3'
    0 row(s) in 0.0100 seconds

    Here, we insert three values, one at a time. The first insert is at row1, column cf:a, with a value of value1. Columns in HBase are comprised of a column family prefix, cf in this example, followed by a colon and then a column qualifier suffix, a in this case.

Scan the table for all data at once.

    One of the ways to get data from HBase is to scan. Use the scan command to scan the table for data. You can limit your scan, but for now, all data is fetched.

    hbase(main):006:0> scan 'test'
    ROW                                      COLUMN+CELL
     row1                                    column=cf:a, timestamp=1421762485768, value=value1
     row2                                    column=cf:b, timestamp=1421762491785, value=value2
     row3                                    column=cf:c, timestamp=1421762496210, value=value3
    3 row(s) in 0.0230 seconds

Get a single row of data.

    To get a single row of data at a time, use the get command.

    hbase(main):007:0> get 'test', 'row1'
    COLUMN                                   CELL
     cf:a                                    timestamp=1421762485768, value=value1
    1 row(s) in 0.0350 seconds

Disable a table.

    If you want to delete a table or change its settings, as well as in some other situations, you need to disable the table first, using the disable command. You can re-enable it using the enable command.

    hbase(main):008:0> disable 'test'
    0 row(s) in 1.1820 seconds

    hbase(main):009:0> enable 'test'
    0 row(s) in 0.1770 seconds

Disable the table again if you tested the enable command above:

    hbase(main):010:0> disable 'test'
    0 row(s) in 1.1820 seconds

Drop the table.

    To drop (delete) a table, use the drop command.

    hbase(main):011:0> drop 'test'
    0 row(s) in 0.1370 seconds

Exit the HBase Shell.

    To exit the HBase Shell and disconnect from your cluster, use the quit command. HBase is still running in the background.

Server-side Configuration for Simple User Access Operation  

Add the following to the hbase-site.xml file on every server machine in the cluster:

    <property>
      <name>hbase.security.authentication</name>
      <value>simple</value>
    </property>
    <property>
      <name>hbase.security.authorization</name>
      <value>true</value>
    </property>
    <property>
      <name>hbase.coprocessor.master.classes</name>
      <value>org.apache.hadoop.hbase.security.access.AccessController</value>
    </property>
    <property>
      <name>hbase.coprocessor.region.classes</name>
      <value>org.apache.hadoop.hbase.security.access.AccessController</value>
    </property>
    <property>
      <name>hbase.coprocessor.regionserver.classes</name>
      <value>org.apache.hadoop.hbase.security.access.AccessController</value>
    </property>

Client-side Configuration for Simple User Access Operation

Add the following to the hbase-site.xml file on every client:

	<property>
	  <name>hbase.security.authentication</name>
	  <value>simple</value>
	</property>


