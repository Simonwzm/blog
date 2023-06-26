## Summary for `Magx`



> Possible questions:
>
> 1. What question is being studied in this article? Why is this question important?
> 2. what is its core idea?
> 3. what are the advantages of the approach proposed in this paper compared to existing work?
> 4. what do you think are the disadvantages?



### What question is being studied in this article? And its importance?



#### The overall structure of this article

Overall, this paper introduced Magx, a magnetic tracking system featuring its untethered wearability, accuracy, and power efficiency. The following paragraphs mainly revolve around questions about several crucial designs of Magx which contribute to its strong performance, the evaluation of Magx which validates those features we have claimed, and finally, several possible usages supported by Magx which justified its importance in expanding previous ideas and promoting future researches, as well as restating the advantages among similar products.




#### Details of Magx's design

As to the **designs of Magx**, the article mainly elaborates on two aspects: the algorithm design, and the hardware design. 

In the algorithm design section, the author mainly discussed two detailed algorithms that Magx has leveraged: the Tracking algorithm, and the simulation-driven method that tackles *the diminishing Magnet Problems*.

In the tracking algorithm, the team used a dipole model to model the position and movement of the magnet. The team then improved the model by introducing the earth's magnetic field linearly to each magnet we tracked. To solve the function of magnets' position, we use the Levenberg-Marquardt algorithm and use a sliding window filter, and a Kalman filter to reduce noise.

On tackling *the diminishing Magnet Problems*, the team used a simulation-driven method and an SVM classifier to detect if there is a magnet occurred magnetic field within the set range, and hence change the mode of MagX between idles and active. Such improvements contribute to Magx's power efficiency and accuracy.


In the **Hardware design section**, the team introduced its `CAMAD Pipeline Design` and the Hardware Configuration. 

`CAMAD Pipeline Design`, namely a Computer-aided magnetometer array design, features a specially designed magnetic sensor layout.  The team developed a two-layer, eight-sensors layout for their backend device. The distances between the two layers and between sensors are optimized carefully and testified through various examinations, which are intended for maximizing portability as well as not sacrificing the accuracy of detecting magnetic fields in the long range.

As for the hardware configuration, the team highlights two points in their research: the selection of magnetometer sensors and their supporting Bluetooth communication protocols, and the magnetometer calibration algorithm.  Both measures are proved to minimize noise and maximize the resolution of the magnetic field measurements.



#### The importance of Magx

**The importance of Magx embodies its advanced performance among similar products and its broad range of applications**.

By comparing with similar products in the market, Magx shows an equally strong performance in accuracy compared with LOS-based methods, and equally strong protection of privacy compared to inertial-based products, meanwhile highlighting its untethered wearability and its low power consumption.  

The team designed several use cases which emphasize Magx's importance. 

For example, Magx can be introduced in face-touching detection. Considering serious pandemic prevention situations in most countries, Magx can offer a fine-grained, training-free, and highly usable choice for face-touching tracking, which can largely reduce the spread of the virus. On the other hand, unconscious face-touching behavior such as nail biting and hair curving can also be detected, which may help users correct their bad habits.

Other usages of Magx including controller-free AR Interaction and endocapsule tracking are also of great significance to the current industry. These further support the importance of Magx



### What is the article's core idea?

The core idea of this article is to introduce the advanced design of Magx and provide possible applications for Magx. The team also hopes that this development can inspire further adoption and exploration of magnetic sensing.



### What are the advantages of the approach proposed in this article compared to existing works?

Overall speaking, Magx features its accuracy and wide range adaptivity in magnetic field detecting, its untethered wearability, and its low power overheads.

Magx adopted a magnet filed detecting method which tracks the spatial positions of passive magnets. In particular, the team conducted a detailed comparison between Magx and existing works in two aspects, the first compares the hand tracking effects of different existing tracking methods including the magnetic field detection we adopted, and the second compares the tracking effect of different methods of detecting magnets in magnetic field detection.

















