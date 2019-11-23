# rogue AP detection 

We assume an environment where an unauthorized AP can lead to compromise of sensitive data or services. To prevent this, we scan for any network which not created by the network administrator. We do this by placing probes (Raspberry Pi) which scan WiFi networks in range. If a network with an allowed SSID is found, it is further verified by connecting to it and checking 802.1X certificate. Rogue AP's position is approximated using trilateration from the probes.
For testing, we used two APs (both Turris MOX). The first one was running a FreeRadius server and at the same time serving as a WPA2 enterprise AP. The second one represented the attacker's AP. The setup was identical except for a different CA and server certificate. For running the probes, we used Raspberry Pi. We used Python for the probes software.
On the probes, we make periodic scans and report the rogue APs to a central server via HTTP. When a rogue AP is detected, the server sends requests to all probes to report signal strength to the suspicious AP. Results are plotted and presented via a web interface.
Steps

   * setup and place Radius server and WPA2 Enterprise AP (https://github.com/ouaibe/howto/blob/master/OpenWRT/802.1xOnOpenWRTUsingFreeRadius.md might be helpful when using OpenWRT)  
   * setup rogue AP - replicate the setup from the previous step but this time generate another CA and server certificate  
   * setup central monitoring server  
   * place Raspberry Pi probes and setup probing daemon with the correct central server IP  
