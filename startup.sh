# CREDITS DEVS EXPO
nowtime=$(date)
echo "
@ANDENCENTO USERBOT
(C) @ANDENCENTO
Powered By @ANDENCENTO.
Time : $nowtime
"
update_and_install_packages () {
    apt -qq update -y
    apt -qq install -y --no-install-recommends \
        git \
        ffmpeg \
        mediainfo \
        unzip \
        wget \
        gifsicle 
  }
ech_final () {
    echo "
    
=+---------------------------------------------------------+=
Deployment Sucessfull.
Docker Images Are Being Pushed, Please Wait.
=+---------------------------------------------------------+=
    "
}

_run_all () {
    update_and_install_packages
    install_helper_packages
    pip3 install –upgrade pip
    pip3 install --no-cache-dir -r requirements.txt
    ech_final
}

_run_all
