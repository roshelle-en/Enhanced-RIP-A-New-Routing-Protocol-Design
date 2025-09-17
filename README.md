# Enhanced-RIP-A-New-Routing-Protocol-Design
This project involves designing and simulating a new routing protocol design that enhances the traditional Routing Information Protocol (RIP) by addressing its well-known limitations:

Simplistic metric (hop count only)

Slow convergence during topology changes or failures

Lack of built-in security

The enhanced protocol proposes multi-metric routing, precomputed backup paths, and lightweight security mechanisms while retaining RIP’s simplicity and backward compatibility.

🚀 Key Enhancements
1. Composite Metric (Compound Cost)

Traditional RIP only considers hop count when selecting routes, often leading to poor performance in modern networks.
Our solution introduces a compound cost formula that incorporates multiple performance factors:

𝑀
𝑒
𝑡
𝑟
𝑖
𝑐
=
𝑎
0
⋅
𝐻
𝑜
𝑝
𝐶
𝑜
𝑢
𝑛
𝑡
+
𝑎
1
⋅
1
𝐵
𝑎
𝑛
𝑑
𝑤
𝑖
𝑑
𝑡
ℎ
+
𝑎
2
⋅
𝐷
𝑒
𝑙
𝑎
𝑦
+
𝑎
3
⋅
𝐽
𝑖
𝑡
𝑡
𝑒
𝑟
+
𝑎
4
⋅
𝑃
𝑎
𝑐
𝑘
𝑒
𝑡
𝐿
𝑜
𝑠
𝑠
Metric=a
0
	​

⋅HopCount+a
1
	​

⋅
Bandwidth
1
	​

+a
2
	​

⋅Delay+a
3
	​

⋅Jitter+a
4
	​

⋅PacketLoss

Hop Count: Basic RIP-style metric (1–15)

Bandwidth: Higher bandwidth is prioritized by using the inverse value

Delay (RTT): Latency measurement using lightweight probes

Jitter (optional): Variation in delay

Packet Loss (optional): Reliability indicator

Weights (a0–a4): Configurable by administrators to prioritize specific needs

👉 This enables flexible routing decisions for high-throughput, low-latency, or reliability-focused networks.



2. Primary and Secondary Node Sets

RIP traditionally maintains only one next hop per destination. Our design introduces:

Primary Next Hop: Best route using compound cost

Secondary Node Set: Precomputed backup paths stored in a min-heap structure

🔹 Benefits:

Fast rerouting upon failures

No need for recomputation during packet forwarding

Backup paths ranked by compound cost 

3. Failure-Aware Forwarding

Packets carry failure data in their headers, which includes failed links/nodes.

When a router detects a failure, it updates the packet header.

Downstream routers avoid failed paths by choosing the next-best option from the secondary set.

Provides proactive rerouting instead of waiting for periodic updates


4. Memory Optimization

Maintaining multiple paths can increase memory usage. To mitigate this:

Limit secondary nodes to k entries (based on average node degree).

Dynamic pruning: Remove unused secondary entries after 90 seconds (3 RIP cycles).

This balances resilience with efficiency.


5. Security with HMAC

RIP lacks authentication and is vulnerable to spoofing and black-hole attacks.
We integrated HMAC-SHA1 to secure routing updates:

Pre-Shared Key (PSK): 256-bit secret shared among routers

HMAC Field: 20-byte SHA1 digest appended to each packet

Verification: Updates are processed only if the HMAC is valid

🔹 This protects against:

False route injection

Replay attacks

Traffic hijacking


⚙️ Router Operation Flow

Initialization

Configure PSK, compound cost weights, and secondary set size (k)

Initialize routing tables

Metric Collection

Measure bandwidth, delay, jitter, and packet loss to neighbors

Routing Table Construction

Compute compound costs

Select primary and secondary next hops

Periodic Updates (every 30s)

Broadcast routing updates with compound costs and HMAC authentication

Apply pruning to secondary sets

Forwarding Process

Verify HMAC

Check primary hop availability

If failed, switch to secondary hop set

Update failure data in packet header


📊 Simulations and Results

We validated our design through Python-based simulations (NetworkX + custom algorithms).

1. Path Selection

Standard RIP selected shortest-hop paths that were suboptimal in delay/bandwidth.

Enhanced RIP selected higher quality paths, considering bandwidth and delay.

2. Convergence Time

Standard RIP: Slow recovery after failures due to periodic updates.

Enhanced RIP: Immediate rerouting using precomputed secondary sets.

3. Security Simulation

Without HMAC: Malicious node successfully injected false routes (black-hole attack).

With HMAC: Malicious updates were rejected, preventing hijacking.

📈 Scalability Analysis

Computational Complexity:

Compound cost: O(n) per neighbor

Secondary node set: O(k log k) per destination

Memory Usage: O(D · (1 + k)), bounded by pruning and fixed k

Network Growth:

Still limited to 15 hops (RIP constraint)

Improved path quality through multi-metric evaluation

Backward compatible with legacy RIP

✅ Advantages of the Enhanced RIP

🎯 Better QoS: Routes optimized for bandwidth, delay, and reliability

⚡ Fast Convergence: Secondary nodes enable immediate rerouting

🔒 Secure: HMAC prevents malicious updates

🛠 Backward Compatible: Works alongside legacy RIP

💡 Scalable & Efficient: Controlled memory and CPU overhead

📚 References

RFC 2453: RIP Version 2

RFC 4822: RIPv2 Cryptographic Authentication

Cloudflare – What is BGP?

GeeksforGeeks – Routing Protocols Overview

📌 Future Work

Extend to hierarchical designs for larger networks (area-based segmentation like OSPF)

Replace HMAC-SHA1 with HMAC-SHA256 for stronger cryptographic security

Adaptive weight tuning based on traffic type (QoS classes)

Integration with SDN controllers for dynamic reconfiguration

🤝 Contributions

This project was developed as part of a research and design study on improving distance-vector routing protocols.
