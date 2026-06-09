# Module 09: SDN and Cloud Networking

[← Previous](../08_network-security/) | [Topic Home](../../README.md) | [Next →](../10_network-programming/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-blue)
![Time](https://img.shields.io/badge/time-5h-orange)

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

---

## Overview

Software-Defined Networking (SDN) separates the network control plane (deciding where traffic goes) from the data plane (actually forwarding packets), enabling programmatic network management. Cloud networking builds on these principles to create virtual networks (VPCs) that provide isolation, security, and flexibility at massive scale. This module covers SDN concepts, OpenFlow, AWS VPC architecture, and overlay networking with VXLAN.

---

## Prerequisites

- Module 03: IP Networking — subnetting, routing, NAT
- Module 06: Routing Protocols — BGP (used in cloud networking internally)
- Module 08: Network Security — security groups, firewalls

---

## Objectives

By the end of this module, you will be able to:

1. Explain the SDN architecture: separation of control and data planes, the role of a controller
2. Describe how OpenFlow enables programmatic forwarding rule management
3. Explain AWS VPC architecture: subnets, route tables, internet gateway, security groups, NACLs
4. Describe VXLAN and why overlay networks are necessary in cloud environments
5. Compare BGP EVPN as a control plane for VXLAN in large-scale deployments

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be written in a future update.

### Software-Defined Networking

Traditional networking: each switch/router has its own control plane (routing protocol, configuration) and data plane (forwarding hardware). SDN separates these:

- **Control plane:** centralized SDN controller (e.g., OpenDaylight, ONOS); has a global view of the network
- **Data plane:** simple forwarding devices (OpenFlow switches); execute rules programmed by the controller
- **Southbound API:** between controller and switches (OpenFlow is the most common protocol)
- **Northbound API:** between controller and applications (REST APIs, intent-based interfaces)

Benefits: programmable, vendor-neutral, enables traffic engineering, rapid policy changes.

### OpenFlow

OpenFlow is the most widely deployed SDN southbound protocol. Controllers send flow tables to switches; each flow table entry specifies:
- **Match fields:** packet header fields (src/dst IP, port, VLAN, etc.)
- **Actions:** forward to port, drop, modify headers, send to controller

When a packet arrives at an OpenFlow switch, it matches against flow table entries. If no match, the packet is sent to the controller for a decision.

### AWS VPC Architecture

A Virtual Private Cloud (VPC) is a logically isolated network in AWS. Key components:

```
AWS Region
  └── VPC (e.g., 10.0.0.0/16)
        ├── Availability Zone A
        │     ├── Public Subnet (10.0.1.0/24)
        │     │     └── Internet Gateway → Internet
        │     └── Private Subnet (10.0.2.0/24)
        │           └── NAT Gateway → Internet (outbound only)
        └── Availability Zone B
              ├── Public Subnet (10.0.3.0/24)
              └── Private Subnet (10.0.4.0/24)
```

Key AWS networking concepts:
- **Security Groups:** stateful instance-level firewall (allow rules only; deny is default)
- **NACLs (Network Access Control Lists):** stateless subnet-level firewall (allow and deny rules; applied to subnet)
- **Route Tables:** control routing within and between subnets; each subnet associated with one route table
- **Internet Gateway:** NAT/routing for public subnets; allows two-way internet communication
- **NAT Gateway:** allows private subnet instances to initiate outbound internet connections; blocks unsolicited inbound

### VXLAN — Virtual Extensible LAN

VXLAN (RFC 7348) is an overlay network protocol that encapsulates Ethernet frames inside UDP packets, allowing Layer 2 networks to span Layer 3 boundaries.

```
Original Ethernet Frame
  └── Encapsulated in VXLAN header (8 bytes: VNI + flags)
        └── Encapsulated in UDP (destination port 4789)
              └── Encapsulated in IP (transport network)
```

The VXLAN Network Identifier (VNI) is a 24-bit field — up to 16 million virtual network segments (vs. 4094 VLANs). This is why VXLAN is used in data centers and cloud environments where VLANs would be exhausted.

AWS, GCP, and Azure all use overlay networks internally (often VXLAN or proprietary variants) to create the illusion of isolated Layer 2 networks for millions of customer VPCs on shared physical infrastructure.

---

## Key Concepts

**Control plane** — The part of a network device that makes routing/forwarding decisions. In SDN, this is centralized in a controller.

**Data plane** — The part that actually forwards packets based on rules provided by the control plane.

**VPC** — Virtual Private Cloud; a customer-isolated virtual network in a public cloud, implemented using SDN and overlay networking.

**Security group** — Stateful virtual firewall in AWS; rules specify allowed traffic; implicit deny for everything else.

**NACL** — Network Access Control List; stateless firewall at the subnet level in AWS; evaluates rules in order; has explicit deny rules.

**VXLAN** — Virtual Extensible LAN; overlay protocol encapsulating Ethernet frames in UDP for transport across Layer 3 networks; 24-bit VNI allows 16M segments.

**BGP EVPN** — Ethernet VPN; uses BGP as the control plane to distribute MAC/IP reachability information for VXLAN; used in large-scale data center networking.

---

## Examples

```bash
# AWS CLI: list VPCs and subnets
aws ec2 describe-vpcs --query 'Vpcs[*].{VpcId:VpcId,CIDR:CidrBlock,Name:Tags[?Key==`Name`]|[0].Value}'
aws ec2 describe-subnets --query 'Subnets[*].{SubnetId:SubnetId,CIDR:CidrBlock,AZ:AvailabilityZone}'

# Show VXLAN interfaces on Linux
ip link show type vxlan

# Create a VXLAN interface (requires root)
ip link add vxlan100 type vxlan id 100 dstport 4789 dev eth0
ip addr add 10.100.0.1/24 dev vxlan100
ip link set vxlan100 up
```

```python
# Using boto3 to list AWS VPC route tables
import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')

response = ec2.describe_route_tables()
for rt in response['RouteTables']:
    print(f"Route Table: {rt['RouteTableId']}")
    for route in rt['Routes']:
        dest = route.get('DestinationCidrBlock', 'N/A')
        gateway = route.get('GatewayId', route.get('NatGatewayId', 'local'))
        print(f"  {dest} → {gateway}")
```

---

## Common Pitfalls

**Security group vs NACL confusion:** Security groups are stateful (if you allow outbound, inbound replies are automatically allowed). NACLs are stateless (you must explicitly allow both inbound and outbound for bidirectional communication). Using NACLs as if they were stateful is a common misconfiguration.

**Overlooking inter-VPC routing:** VPCs are isolated by default. Communicating between VPCs requires VPC Peering, AWS Transit Gateway, or an overlay VPN. Traffic between peered VPCs does NOT traverse the internet; it uses AWS's backbone.

**Forgetting that VXLAN adds overhead:** Each VXLAN frame has ~50 bytes of additional headers. If your underlying network MTU is 1500, your inner frames must be limited to ~1450 bytes to avoid fragmentation. Set jumbo frames (MTU 9000) in the transport network to avoid this.

---

## Cross-Links

- [[networks/modules/03_ip-networking]] — VPC subnetting uses CIDR; routing tables and NAT concepts apply directly
- [[networks/modules/08_network-security]] — Security groups and NACLs are the application of firewall concepts in cloud
- [[networks/modules/02_physical-and-datalink]] — VLANs vs VXLAN; why 4094 VLANs are insufficient at cloud scale
- [[devops-platform-engineering]] — VPCs, security groups, and load balancers are core DevOps infrastructure

---

## Summary

- SDN separates control plane (decisions) from data plane (forwarding); enables programmatic, vendor-neutral network management
- OpenFlow: controller programs flow tables in switches; match fields + actions; packets with no match sent to controller
- AWS VPC: isolated virtual network; public/private subnets; internet gateway (public); NAT gateway (private outbound)
- Security Groups: stateful instance-level firewall in AWS; NACLs: stateless subnet-level firewall in AWS
- VXLAN: encapsulates Ethernet frames in UDP; 24-bit VNI allows 16M segments; enables Layer 2 over Layer 3 (overlays)
- BGP EVPN: BGP used as VXLAN control plane to distribute MAC/IP info at scale in data centers
