FROM gitpod/workspace-full
USER gitpod
RUN sudo apt-get update -q && sudo apt-get upgrade && sudo apt install ncdu ffmpeg tmux

