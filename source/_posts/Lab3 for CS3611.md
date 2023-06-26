# Lab3 for CS3611

<div style='text-align:center;'>王梓萌 521030910015</div>



## 

### 

![image-20230502230726961](C:\Users\simon\AppData\Roaming\Typora\typora-user-images\image-20230502230726961.png)



**Solution**

The code named `topo.py` is used to create the net as above.

The screenshot of mininet is given below:

![image-20230503003918834](C:\Users\simon\AppData\Roaming\Typora\typora-user-images\image-20230503003918834.png)



### 

![image-20230502232612348](C:\Users\simon\AppData\Roaming\Typora\typora-user-images\image-20230502232612348.png)



**Solution**

Detailed implementation is in the code. The screenshot of this chatting room is as follow:

![image-20230502233624450](C:\Users\simon\AppData\Roaming\Typora\typora-user-images\image-20230502233624450.png)

In `user` and program, to avoid congestion in socket, we set the socket to no_congestion mode. To both listening the server's message and user's input, we use `select()` and monitor file descriptors for activity. If file_descriptor of our socket is modified, an incoming message is received. If it is not and we receive modification in stdin, then user's input is incoming.

In `center` , the program stores an `ip-hostname` table to identify the sender and target hostname from incoming TCP message. Then socket programming is used to receive message, and redirect it to the specified host. First we establish a listening socket and wait for incoming connection. Whenever a new connection is accepted, a new socket is assigned to this connection and the socket_file_descriptor is recorded. Then we still use the similar trick to both listening and operating the message in each connection. We use ` select()` and monitor file descriptors for activity. If file_descriptor of our socket is modified, an incoming message is received. If it is not and we receive modification in stdin, then user's input is incoming. The difference between client and server is that server has multiply socket and its file_descriptor to maintain, so another mapping from socket_file_descriptor to hostname/IP is required. 

The detailed implementation is in the code.



## 

### 

![image-20230502235701314](C:\Users\simon\AppData\Roaming\Typora\typora-user-images\image-20230502235701314.png)

**Solution** 

The general network topology is the same as problem 1. But to enable broadcasting which is used by our udp program, we need to add additional codes to achieve this , which is 

```python
for i in range(1, 6):
    host = net.get('h%d' % i)
    host.cmd('route add -net 10.0.0.0 netmask 255.255.255.0 broadcast 10.0.0.255 dev h%d-eth0' % i)

```

The total python code is as below:

```python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Controller
from mininet.log import setLogLevel

class SimpleTopo(Topo):
    def build(self):
        switch = self.addSwitch('s1')

        for i in range(1, 6):
            host = self.addHost('h%d' % i, ip='10.0.0.%d/24' % i)
            self.addLink(host, switch)

def run_topo():
    topo = SimpleTopo()
    net = Mininet(topo=topo, controller=Controller)
    net.start()

    # Configure broadcast IP for each host
    for i in range(1, 6):
        host = net.get('h%d' % i)
        host.cmd('route add -net 10.0.0.0 netmask 255.255.255.0 broadcast 10.0.0.255 dev h%d-eth0' % i)

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run_topo()

```



The screenshot of creating the network is shown below:

![image-20230503000723259](C:\Users\simon\AppData\Roaming\Typora\typora-user-images\image-20230503000723259.png)





### 

![image-20230503000055669](C:\Users\simon\AppData\Roaming\Typora\typora-user-images\image-20230503000055669.png)

In this sub-question a program without self IP filtering is required. 

The screenshot is shown below:
![image-20230503000628085](C:\Users\simon\AppData\Roaming\Typora\typora-user-images\image-20230503000628085.png)



Note that the question does not specifically require the hostname to be identified, but for the convenience of the next problem in which we are going to filter out our own IP's message, we in advance identified the ip of messages from broadcast address. We can collect the sender's IP by method `recv_from` and it fills the `sockaddr_in` structure that contains the sender's address field. We then printed it in the terminal.

The program is based on udp because the socket is created using udp method:

```c++
int sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
```

Only one socket is created and it is responsible for both sending and receiving message from the broadcast address. Again to avoid congestion of both listening and sending message in one socket, we use `select()` and monitor the socket's file_descriptor to notice an incoming message. The detailed method has been introduced before.

Because the message is sent to the broadcast address, all other client will be able to receive the message.



### 

To filter out the message from ourselves, we need to identify the sender's IP and compare it with the IP of the device running the current client.

The extraction of IP from incoming message is implemented in the previous question. Now we need to fetch the local device's IP. The detailed code is given below:

```c++
set<string> get_local_ips() {
    set<string> local_ips;
    struct ifaddrs* ifaddr;

    if (getifaddrs(&ifaddr) == -1) {
        cerr << "Error retrieving local IP addresses." << endl;
        return local_ips;
    }

    for (struct ifaddrs* ifa = ifaddr; ifa != nullptr; ifa = ifa->ifa_next) {
        if (ifa->ifa_addr == nullptr) {
            continue;
        }

        if (ifa->ifa_addr->sa_family == AF_INET) {
            char ip[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &(((struct sockaddr_in*)ifa->ifa_addr)->sin_addr), ip, INET_ADDRSTRLEN);
            local_ips.insert(string(ip));
        }
    }

    freeifaddrs(ifaddr);
    return local_ips;
}
```



When receiving an incoming message, we filter out the message that has the same IP with local_IPs. Other parts of the code remain the same.

The detailed implementation is given in the code, <span style='color:red'>**under a new file_name: udp_imprv.cpp**</span>.

The screenshot is given below:

![image-20230503003817888](C:\Users\simon\AppData\Roaming\Typora\typora-user-images\image-20230503003817888.png)







