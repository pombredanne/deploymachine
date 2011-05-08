
__description__ = "Memcached shared memory cache daemon"
__config__ = {
    "memcached.memory": dict(
        description = "Memory allocated for memcached instance in megabytes",
        default = 64,
    ),
    "memcached.listen_address": dict(
        description = "IP address to bind to",
        default = "127.0.0.1",
    ),
    "memcached.port": dict(
        description = "Port to use for memcached instance",
        default = 11211,
    ),
    "memcached.user": dict(
        description = "User as which to run the memcached instance",
        default = "nobody",
    ),
    "memcached.threads": dict(
        description = "Number of threads to use to process incoming requests",
        default = 1,
    ),
    "memcached.verbose": dict(
        description = "Verbose logging output",
        default = False,
    ),
}
