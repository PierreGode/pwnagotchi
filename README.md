<p align="center">
  <small>Join the project community on our server!</small>
  <br/><br/>
  <a href="https://discord.gg/https://discord.gg/btZpkp45gQ" target="_blank" title="Join our community!">
    <img src="https://dcbadge.limes.pink/api/server/https://discord.gg/btZpkp45gQ"/>
  </a>
</p>
<hr/>

<p align="center">
    <a href="https://github.com/evilsocket/pwnagotchi/releases/latest"><img alt="Release" src="https://img.shields.io/github/release/evilsocket/pwnagotchi.svg?style=flat-square"></a>
    <a href="https://github.com/evilsocket/pwnagotchi/blob/master/LICENSE.md"><img alt="Software License" src="https://img.shields.io/badge/license-GPL3-brightgreen.svg?style=flat-square"></a>
    <a href="https://github.com/evilsocket/pwnagotchi/graphs/contributors"><img alt="Contributors" src="https://img.shields.io/github/contributors/evilsocket/pwnagotchi"/></a>
    <a href="https://twitter.com/intent/follow?screen_name=pwnagotchi"><img src="https://img.shields.io/twitter/follow/pwnagotchi?style=social&logo=twitter" alt="follow on Twitter"></a>
    <br/>
    <br/>
    <img src="https://www.evilsocket.net/images/human-coded.png" height="30px" alt="This project is 100% made by humans."/>

</p>

[Pwnagotchi](https://pwnagotchi.ai/) is an [actor-critic](https://hackernoon.com/intuitive-rl-intro-to-advantage-actor-critic-a2c-4ff545978752) *(currently a recurrent PPO implementation powered by Stable-Baselines3)* "AI" leveraging [bettercap](https://www.bettercap.org/) that learns from its surrounding WiFi environment to maximize the crackable WPA key material it captures (either passively, or by performing authentication and association attacks). This material is collected as PCAP files containing any form of handshake supported by [hashcat](https://hashcat.net/hashcat/), including [PMKIDs](https://www.evilsocket.net/2019/02/13/Pwning-WiFi-networks-with-bettercap-and-the-PMKID-client-less-attack/), 
full and half WPA handshakes.

![ui](https://i.imgur.com/X68GXrn.png)

Instead of merely playing [Super Mario or Atari games](https://becominghuman.ai/getting-mario-back-into-the-gym-setting-up-super-mario-bros-in-openais-gym-8e39a96c1e41?gi=c4b66c3d5ced) like most reinforcement learning-based "AI" *(yawn)*, Pwnagotchi tunes [its parameters](https://github.com/evilsocket/pwnagotchi/blob/master/pwnagotchi/defaults.toml) over time to **get better at pwning WiFi things to** in the environments you expose it to. 

More specifically, Pwnagotchi is using an [LSTM with MLP feature extractor](https://sb3-contrib.readthedocs.io/en/master/modules/sb3_contrib.common.recurrent.policies.html) as its policy network for a [Recurrent PPO agent](https://sb3-contrib.readthedocs.io/en/master/modules/sb3_contrib.ppo_recurrent.html) built on top of [Stable-Baselines3](https://stable-baselines3.readthedocs.io/). If you're unfamiliar with PPO/A2C style actor-critic methods, here is [a very good introductory explanation](https://hackernoon.com/intuitive-rl-intro-to-advantage-actor-critic-a2c-4ff545978752) (in comic form!) of the basic principles behind how Pwnagotchi learns. (You can read more about how Pwnagotchi learns in the [Usage](https://www.pwnagotchi.ai/usage/#training-the-ai) doc.)

**Keep in mind:** Unlike the usual RL simulations, Pwnagotchi learns over time. Time for a Pwnagotchi is measured in epochs; a single epoch can last from a few seconds to minutes, depending on how many access points and client stations are visible. Do not expect your Pwnagotchi to perform amazingly well at the very beginning, as it will be [exploring](https://hackernoon.com/intuitive-rl-intro-to-advantage-actor-critic-a2c-4ff545978752) several combinations of [key parameters](https://www.pwnagotchi.ai/usage/#training-the-ai) to determine ideal adjustments for pwning the particular environment you are exposing it to during its beginning epochs ... but ** listen to your Pwnagotchi when it tells you it's boring!** Bring it into novel WiFi environments with you and have it observe new networks and capture new handshakes—and you'll see. :)

Multiple units within close physical proximity can "talk" to each other, advertising their presence to each other by broadcasting custom information elements using a parasite protocol I've built on top of the existing dot11 standard. Over time, two or more units trained together will learn to cooperate upon detecting each other's presence by dividing the available channels among them for optimal pwnage.

## Platform Support (2025 refresh)

- **Operating system:** the builder now targets the official Debian 13 (Trixie) 64-bit Raspberry Pi images published at [raspi.debian.net](https://raspi.debian.net/). Legacy Raspbian-specific tweaks (kali-pi kernels, armhf builds, etc.) have been removed.
- **Python runtime:** the codebase, packaging metadata, and dependencies were audited for CPython 3.13 compatibility. Runtime testing is still performed on 3.10–3.13, but new features are developed and linted with 3.13 to ensure future Debian releases keep working out of the box.
- **AI stack:** TensorFlow 1.x and the original `stable-baselines` dependency have been retired in favor of PyTorch, Stable-Baselines3, and the `sb3-contrib` recurrent PPO implementation.

### Building refreshed images

The `Makefile` exposes two new knobs so you can pin the exact Debian image and checksum you want to trust:

```bash
make BASE_IMAGE_URL=https://raspi.debian.net/daily/raspi_4_trixie.img.xz \
  BASE_IMAGE_CHECKSUM=sha256:YOUR_CHECKSUM_HERE image
```

The defaults already point to the rolling daily Trixie builds, but you should always update `BASE_IMAGE_CHECKSUM` with the value published alongside the image you downloaded.

## Documentation

https://www.pwnagotchi.ai

## Links

&nbsp; | Official Links
---------|-------
Website | [pwnagotchi.ai](https://pwnagotchi.ai/)
Forum | [community.pwnagotchi.ai](https://community.pwnagotchi.ai/)
Slack | [pwnagotchi.slack.com](https://invite.pwnagotchi.ai/)
Subreddit | [r/pwnagotchi](https://www.reddit.com/r/pwnagotchi/)
Twitter | [@pwnagotchi](https://twitter.com/pwnagotchi)

## License

`pwnagotchi` is made with ♥  by [@evilsocket](https://twitter.com/evilsocket) and the [amazing dev team](https://github.com/evilsocket/pwnagotchi/graphs/contributors). It is released under the GPL3 license.
