CREATE EXTERNAL TABLE IF NOT EXISTS vpc_flow_logs_tgw_attachment_outbound (
    version int,
    resource_type string,
    account_id string,
    tgw_id string,
    tgw_attachment_id string,
    tgw_src_vpc_account_id string,
    tgw_dst_vpc_account_id string,
    tgw_src_vpc_id string,
    tgw_dst_vpc_id string,
    tgw_src_subnet_id string,
    tgw_dst_subnet_id string,
    tgw_src_eni string,
    tgw_dst_eni string,
    tgw_src_az_id string,
    tgw_dst_az_id string,
    tgw_pair_attachment_id string,
    srcaddr string,
    dstaddr string,
    srcport int,
    dstport int,
    protocol bigint,
    packets bigint,
    bytes bigint,
    start bigint,
    `end` bigint,
    log_status string,
    type string,
    packets_lost_no_route bigint,
    packets_lost_blackhole bigint,
    packets_lost_mtu_exceeded bigint,
    packets_lost_ttl_expired bigint,
    tcp_flags int,
    region string,
    flow_direction string,
    pkt_src_aws_service string,
    pkt_dst_aws_service string
)
PARTITIONED BY (day string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '
LOCATION 's3://your-flow-logs-bucket/path-to-logs/'
TBLPROPERTIES (
    "skip.header.line.count" = "1",
    "projection.enabled" = "true",
    "projection.day.type" = "date",
    "projection.day.range" = "2025/01/01,NOW",
    "projection.day.format" = "yyyy/MM/dd",
    "storage.location.template" = "s3://your-flow-logs-bucket/path-to-logs/${day}"
);