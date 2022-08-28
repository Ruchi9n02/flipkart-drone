# IROS 2022 Safe Robot Learning Competition

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/bWhDTNtj8EA/maxresdefault.jpg)](https://www.youtube.com/watch?v=bWhDTNtj8EA)

*Note: beta release subject to change throughout the month of August 2022; register for updates*

- [Official Webpage](https://www.dynsyslab.org/iros-2022-safe-robot-learning-competition/)
- [IROS Competition Page](https://iros2022.org/program/competition/#toggle-id-8)
- [GitHub Discussions](https://github.com/utiasDSL/safe-control-gym/discussions/categories/iros-2022-competition)
- [Google Form](https://forms.gle/vEmVK99n1SyaE4Zw9) (to register your interest and receive e-mail updates)

## Description 

The task is to design a controller/planner that enables a quadrotor (*Crazyflie 2.x*) to **safely fly through a set of gates and reach a predefined target despite uncertainties in the robot dynamics (e.g., mass and inertia) and the environment (e.g., wind and position of the gates)**. The algorithms will be evaluated regarding their safety (e.g., no collisions) and performance (e.g., time to target). We encourage participants to explore both control and reinforcement learning approaches (e.g., robust, adaptive, predictive, learning-based and optimal control, and model-based/model-free reinforcement learning). The controller/planner has access to the position and attitude measurements provided by a motion capture system and the noisy pose of the closest next gate. The controller can [send position, velocity, acceleration and heading references to an onboard position controller](https://crazyswarm.readthedocs.io/en/latest/api.html#pycrazyswarm.crazyflie.Crazyflie.cmdFullState).

## Install on Ubuntu/macOS

We recommend Ubuntu 20.04 on a mid-tier laptop and GPU (e.g., a Lenovo P52 with i7-8850H/Quadro P2000)

```bash
git clone https://github.com/utiasDSL/safe-control-gym.git
cd safe-control-gym
git checkout beta-iros-competition
```

Create and access a Python 3.8 environment using
[`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

```bash
conda create -n safe python=3.8
conda activate safe
```

Install the `safe-control-gym` repository 

```
pip install --upgrade pip
pip install -e .
```

## Install `pycffirmware` (optional, recommended) 

```bash
git clone https://github.com/utiasDSL/pycffirmware.git
cd pycffirmware/
git submodule update --init --recursive
```

### On Ubuntu

```
sudo apt update
sudo apt -y install swig
sudo apt install build-essential
cd wrapper
chmod +x build_linux.sh
conda activate safe
./build_linux.sh
```

### On macOS

Install [`brew`](https://brew.sh/), then
```
brew install swig
brew install gcc            # Also run `xcode-select --install` if prompted
brew install make
cd wrapper
chmod +x build_osx.sh       # Assumes `gcc` is at `/usr/local/bin/gcc-12`
conda activate safe
./build_osx.sh
```

Also see how to install [SWIG](https://www.dev2qa.com/how-to-install-swig-on-macos-linux-and-windows/) and [`pycffirmware`](https://github.com/utiasDSL/pycffirmware)'s `README.md`

## Getting Started
Run the scripts in [`competition/`](https://github.com/utiasDSL/safe-control-gym/tree/main/competition)
```bash
cd ./competition/
python3 getting_started.py --overrides ./getting_started.yaml
```
**Modify file [`edit_this.py`](https://github.com/utiasDSL/safe-control-gym/blob/beta-iros-competition/competition/edit_this.py) to customize your controller based on [Crazyswarm's Crazyflie interface](https://crazyswarm.readthedocs.io/en/latest/api.html#pycrazyswarm.crazyflie.Crazyflie)**

Also see [section 'Methods to Re-implement'](https://github.com/utiasDSL/safe-control-gym/tree/beta-iros-competition#methods-to-re-implement)

## Submission

- Fork this repo ([help](https://docs.github.com/en/get-started/quickstart/fork-a-repo))
- Checkout this branch (`beta-iros-competition`)
- Implement your solution by modifying [`edit_this.py`](https://github.com/utiasDSL/safe-control-gym/blob/beta-iros-competition/competition/edit_this.py)
- Create a Pull Request into `utiasDSL/safe-control-gym:beta-iros-competition` from your fork ([help](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork))
- Tag @JacopoPan in the Pull Request's Conversation tab

## Methods to Re-implement

Required
```
edit_this.py : Controller.__init__(initial_obs, initial_info)           # Initialize the controller
    Args:
        initial_obs (ndarray): The initial observation of the quadrotor's state
            [x, x_dot, y, y_dot, z, z_dot, phi, theta, psi, p, q, r].
        initial_info (dict): The a priori information as a dictionary with keys
            - 'symbolic_model'                  CasADi's 3D quadrotor dynamics
            - 'symbolic_constraints'            CasADi's constraints
            - 'nominal_physical_parameters'     Nominal mass and inertia
            - 'ctrl_timestep'                   Control timestep (in seconds)
            - 'ctrl_freq'                       Control frequency (in Hz)
            - 'episode_len_sec'                 Maximum duration of an episode (in seconds)
            - 'quadrotor_kf'                    Motor coefficient
            - 'quadrotor_km'                    Motor coefficient
            - 'gate_dimensions'                 Shape and measurements of the gates
            - 'obstacle_dimensions'             Shape and measurements of the obstacles
            - 'nominal_gates_pos_and_type'      Nominal pose and type (tall, low, etc.) of the gates
            - 'nominal_obstacles_pos'           Nominal pose of the obstacles
            - 'x_reference'                     Final position to reach/hover at
            - 'initial_state_randomization'     Distributions of the randomized additive error on the initial pose
            - 'inertial_prop_randomization'     Distributions of the randomized additive error on the inertial properties
            - 'gates_and_obs_randomization'     Distributions of the randomized additive error on the gates and obstacles positions
            - 'disturbances'                    Dynamics and input disturbances's distributions 

    Returns:
        N/A
```

```
edit_this.py : Controller.cmdFirmware(time, obs, reward, done, info)    # Select the next command for the quadrotor
    Args:
        time (float): Episode's elapsed time, in seconds.
        obs (ndarray): The quadrotor's Vicon data
            [x, 0, y, 0, z, 0, phi, theta, psi, 0, 0, 0].
        reward (float, optional): The reward signal.
        done (bool, optional): Wether the episode has terminated.
        info (dict, optional): Current step information as a dictionary with keys
            - 'collision'                       As a tuple (gate id, boolean)
            - 'current_target_gate_id'          Id of the next gate (-1 when all gates have been travelled through)
            - 'current_target_gate_type'        Type of the next gate (0: tall, 1: low, etc.)
            - 'current_target_gate_in_range'    Whether the next gate is close enough for perfect visibility
            - 'current_target_gate_pos'         Nominal or exact position of the next gate (depending on the parameter above)
            - 'at_goal_position'                Whether the quadrotor is at the final position ('x_reference')
            - 'constraint_values'               Constraint evaluation
            - 'constraint_violation'            Whether any of the constraints is violated

    Returns:
        Command: selected type of command (NONE, FULLSTATE, TAKEOFF, LAND, STOP, GOTO, see Enum-like class `Command`).
        List: arguments for the type of command
            - NONE's args: []
            - FULLSTATE's args: [pos (3 val), vel (3 val), acc (3 val), yaw, rpy_rates (3 val), curr_time] 
            - TAKEOFF's args: [height, duration]
            - LAND's args: [height, duration]
            - STOP's args: []
            - GOTO's args: [x, y, z, yaw, duration, relative (bool)]
```

Optional, recommended
```
edit_this.py : Controller.interStepLearn(...)       # Update the controller's internal state at each step
    Args:
        N/A

    Leverage the data in `self.action_buffer`, `self.obs_buffer`, `self.reward_buffer`, self.done_buffer`, `self.info_buffer`

    Returns:
        N/A     
```

```
edit_this.py : Controller.interEpisodeLearn(...)    # Update the controller's internal state between episodes
    Args:
        N/A

    Leverage the data in `self.action_buffer`, `self.obs_buffer`, `self.reward_buffer`, self.done_buffer`, `self.info_buffer`

    Returns:
        N/A
```

## Scoring
1. Performance
- TBA

2. Safety
- TBA

3. Robustness
- TBA

## Prizes
- 1st: TBA
- 2nd: TBA
- 3rd: TBA

## Organizers
- Angela Schoellig (University of Toronto, Vector Institute)
- Davide Scaramuzza (University of Zurich)
- Vijay Kumar (University of Pennsylvania)
- Nicholas Roy (Massachusetts Institute of Technology)
- Todd Murphey (Northwestern University)
- Sebastian Trimpe (RWTH Aachen University)
- Wolfgang Hönig (TU Berlin)
- Mark Muller (University of California Berkeley)
- Jose Martinez-Carranza (INAOE)
- SiQi Zhou (University of Toronto, Vector Institute)
- Melissa Greeff (University of Toronto, Vector Institute)
- Jacopo Panerati (University of Toronto, Vector Institute)
- Yunlong Song (University of Zurich)
- Leticia Oyuki Rojas Pérez (INAOE)
- Adam W. Hall (University of Toronto, Vector Institute)
- Justin Yuan (University of Toronto, Vector Institute)
- Lukas Brunke (University of Toronto, Vector Institute)
- Antonio Loquercio (UC Berkeley)

-----
> University of Toronto's [Dynamic Systems Lab](https://github.com/utiasDSL) / [Vector Institute for Artificial Intelligence](https://github.com/VectorInstitute)
