# rl-solar

## Overview
Applying reinforcement learning to solve a non-stationary modeling and control 
problem for power generation for a dual-axis solar panel.

Complete project details at: https://www.jackogrady.me/reinforcement-learning-solar/project-overview

## Repository Structure

* `firmware/`: holds Arduino firmware as well as interface READMEs for Arduino-Python communication
* `rl_agent/`: holds all code for the final agent design (Softmax Actor-Critic) as well as dev agents
* `schemtics/`: Circuit and system schematics for the project

## Where Should You Start?

Depends what you're looking for! I'd probably recommend going to `> rl_agent > README`, which explains everything about 
the agent and how to run it. If you're more interested in the solar panel and Arduino, head to 
`> firmware > README` to learn about that.

**An Important Note**

This code repository is really meant to be consumed in tandem with the material and the link above. 
At that link, you can read about larger design aspects, concepts, and see experiment results 
(but more importantly, see how everything ties together)

The repository exists so that anyone interested in RL can see an end-to-end implementation of code, 
as well as the experimentation along the way to get to the code.

---
## License

Copyright 2022 Jack O'Grady

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

