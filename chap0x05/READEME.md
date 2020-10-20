##  实验五：基于 Scapy 编写端口扫描器

### 实验目的

- 掌握网络扫描之端口状态探测的基本原理

### 实验环境

+ Virtualbox
+ kali
+ debian

- python3 + [scapy](https://scapy.net/)2.4

### 实验要求

- [x] TCP connect scan / TCP stealth scan
- [x] TCP Xmas scan / TCP fin scan / TCP null scan
- [x] UDP scan
- [x] 上述每种扫描技术的实现测试均需要测试端口状态为：`开放`、`关闭` 和 `过滤` 状态时的程序执行结果
- [x] 提供每一次扫描测试的抓包结果并分析与课本中的扫描方法原理是否相符？如果不同，试分析原因；
- [x] 在实验报告中详细说明实验网络环境拓扑、被测试 IP 的端口状态是如何模拟的
- [x] （可选）复刻 `nmap` 的上述扫描技术实现的命令行参数开关（每种扫描测试一种状态，且后面专门用nmap进行了扫描实验）

### 实验基础

```
iptables -F //清除所有iptables规则

```



### 实验过程

#### 网络拓扑

+ 网管的网卡：内部网络一、NAT转发。
  + 并在网管处配置内部网络一的dns服务器和dhcp服务器。

+ kali：内部网络一
  + 进行扫描的主机。
+ debian2：内部网络一
  + 模拟tcp、udp服务的主机，同时也是被扫描的主机。

<img src="images/image-20201019220008282.png" alt="image-20201019220008282" style="zoom:50%;" />

#### 端口状态模拟

+ **关闭状态**：对应端口关闭

+ **开启状态**：对应端口开启，iptables规则为ACCEPT

  ```bash
  #TCP
  python3 -m http.server //默认8080端口
  //iptables部分规则：
  kate@kate-VirtualBox:~/桌面$ sudo iptables -nv -L INPUT
  Chain INPUT (policy DROP 0 packets, 0 bytes)
   pkts bytes target     prot opt in     out     source               destination         
      4   344 ufw-after-logging-input  all  --  *      *       0.0.0.0/0            0.0.0.0/0           
      4   344 ufw-reject-input  all  --  *      *       0.0.0.0/0            0.0.0.0/0           
      4   344 ufw-track-input  all  --  *      *       0.0.0.0/0            0.0.0.0/0           
  kate@kate-VirtualBox:~/桌面$ 
  
  #UDP
  nc -l -u -p 8000 //开启udp端口
  netstat -antup | grep 8000 //查看8000端口是否启动了UDP监听
  
  nc - vuz 192.168.1.28 80000 //在客户端检测
  //dnsmasq 53端口为UDP
  systemctl dnsmasq restart
  ```

+ **过滤状态**：对应状态开启，iptables 规则为DROP

  ```bash
  #过滤规则
  sudo iptables -I INPUT  -j DROP -p 端口号//过滤所有的tcp的数据包
  
  kate@kate-VirtualBox:~/桌面$ sudo iptables -nv -L INPUT
  Chain INPUT (policy DROP 0 packets, 0 bytes)
   pkts bytes target     prot opt in     out     source               destination         
      0     0            tcp  --  DEROP  *       0.0.0.0/0            0.0.0.0/0           
      2   172 ufw-after-logging-input  all  --  *      *       0.0.0.0/0            0.0.0.0/0           
      2   172 ufw-reject-input  all  --  *      *       0.0.0.0/0            0.0.0.0/0           
      2   172 ufw-track-input  all  --  *      *       0.0.0.0/0            0.0.0.0/0           
  kate@kate-VirtualBox:~/桌面$ 
  ```

#### TCP connect扫描

+ **OPEN**

  <img src="images/TCP_CONNECT_OPEN_RESULT.png" alt="image-20201019192126555"  />

  ![](images/TCP_CONNECT_OPEN_TCPDUMP.png)

  ![img](images/TCP_CONNECT_OPEN_NMAP.png)

+ **CLOSE**

  ![img](images/TCP_CONNECT_CLOSE_SCANER.png)

  ![img](images/TCP_CONNECT_CLOSE_NMAP.png)

  ![TCP_CONNECT_CLOSE](images/TCP_CONNECT_CLOSE.png)

+ **FILTER**

  ```
  #过滤规则
  iptables -I INPUT -p tcp -i DEROP//过滤所有的tcp的数据包
  ```

  ![](images/TCP_CONNECT_FILTERED_RESULT.png)

  ![img](images/TCP_CONNECT_FILTERED_NMAP.png)

  ![img](images/TCP_CONNECT_FILTERED_TCPDUMP.png)

  

#### TCP syn扫描

+ **OPEN**

  <img src="images/TCP_SYN_RESULT.png" alt="image-20201019192126555"  />

  ![](images/TCP_SYN_TCPDUMP.png)

  ![img](images/TCP_SYN_OPEN_NMAP.png)

+ **CLOSE**

  ![img](images/TCP_SYN_CLOSE_RESULT.png)

  ![img](images/TCP_syn_close_nmap.png)

  ![TCP_CONNECT_CLOSE](images/TCP_SYN_CLOSE_TCPDUMP.png)

+ **FILTER**

  ```
  #过滤规则
  iptables -I INPUT -p tcp -i DEROP//过滤所有的tcp的数据包
  ```

  ![image-20201019195053629](images/image-20201019195053629.png)

  ![image-20201019194959709](images/image-20201019194959709.png)

  ![image-20201019195145804](images/image-20201019195145804.png)

#### TCP Xmas扫描

**OPEN**

![image-20201019203347032](images/image-20201019203347032.png)

![image-20201019203606991](images/image-20201019203606991.png)

**CLOSE**

![image-20201019205442309](images/image-20201019205442309.png)

![image-20201019205712445](images/image-20201019205712445.png)

![image-20201019205333692](images/image-20201019205333692.png)

**FILTERED**

![image-20201019202125620](images/image-20201019202125620.png)

![image-20201019201802250](images/image-20201019201802250.png)

![image-20201019202320280](images/image-20201019202320280.png)

#### TCP fin扫描

注：TCP fin 的OPEN和FILTERED的扫描是扫描网关来模拟的（网关ip：192.168.1.1）

**OPEN**

![image-20201020090403248](images/image-20201020090403248.png)

![image-20201020090418777](images/image-20201020090418777.png)

![image-20201020090437993](images/image-20201020090437993.png)

**CLOSE**

![image-20201019205459529](images/image-20201019205459529.png)

![image-20201019205731966](images/image-20201019205731966.png)

![image-20201019205610794](images/image-20201019205610794.png)

**FILTERED**

![image-20201020090726080](images/image-20201020090726080.png)

![image-20201020090743585](images/image-20201020090743585.png)

![image-20201020090757620](images/image-20201020090757620.png)

#### TCP null扫描

**OPEN**

![image-20201019204037896](images/image-20201019204037896.png)

![image-20201019204122574](images/image-20201019204122574.png)

**CLOSE**

![image-20201019205531172](images/image-20201019205531172.png)

![image-20201019205754956](images/image-20201019205754956.png)

![image-20201019205635029](images/image-20201019205635029.png)

**FILTERED**

![image-20201019202428493](images/image-20201019202428493.png)

![image-20201019202542868](images/image-20201019202542868.png)

![image-20201019202559689](images/image-20201019202559689.png)

#### UDP扫描

**OPEN**

![image-20201020103921730](images/image-20201020103921730.png)

![image-20201020103943799](images/image-20201020103943799.png)

![image-20201020104008554](images/image-20201020104008554.png)

**CLOSE**

![image-20201019202628214](images/image-20201019202628214.png)

![image-20201019202714044](images/image-20201019202714044.png)

![image-20201019202952344](images/image-20201019202952344.png)

**FILTERED**

![image-20201020105317205](images/image-20201020105317205.png)

![image-20201020105330750](images/image-20201020105330750.png)

![image-20201020105303033](images/image-20201020105303033.png)

#### 其他实验问题的回答

> 提供每一次扫描测试的抓包结果并分析与课本中的扫描方法原理是否相符？如果不同，试分析原因；

相同。

### 参考

[黄大课件](https://github.com/c4pr1c3/cuc-ns-ppt/blob/master/chap0x05.md)

[2020-ns-public-LyuLumos](https://github.com/CUCCS/2020-ns-public-LyuLumos)