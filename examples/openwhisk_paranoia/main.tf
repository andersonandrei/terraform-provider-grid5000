module "g5k-openwhisk" {
    source = "./modules/g5k-openwhisk"

    username = "adasilva" # Replace by your Grid'5000 username
    nodes_location = "rennes"
    nodes_count = 3
    nodes_selector = "{cluster = 'paranoia'}"
    walltime = "2"

    data_location = "rennes" # rennes or nantes
    ceph_pool_quota = "200G"

    kafka_replicas = 1              # Default: 1, according to available worker nodes
    kafka_persistence_size = "30Gi"   # Default: 20Gi
}

output "wsk_set_apihost" {
    value = "wsk property set --apihost ${module.g5k-openwhisk.wsk_apihost}"
}

output "wsk_set_auth" {
    value = "wsk property set --auth ${module.g5k-openwhisk.wsk_auth}"
}