#!/bin/bash

projectDirectory=ecgWebAnalysisUsingML
echo "current Path: " ${PATH}

echo "Check the directory exists!!\n"
if [[ -d ${projectDirectory} ]]
then
    echo -e ${projectDirectory} "already exists!! Do you want to remove and download again?\n(input \"yes\" to yes or input anything to no)> "
    read answer
    if [[ ${answer} -eq "yes" ]]
    then
	echo "remove " ${HOME}/${projectDirectory}
	rm -rf ${projectDirectory}
	echo -e "Download the github repository!!\n"
	git clone https://github.com/incognito-developer/ecgAnalysisUsingML.git ${projectDirectory}

    else
	echo "pass remove directory and not download!!"
    fi

else
    echo "Download the github repository!!\n"
    git clone https://github.com/incognito-developer/ecgAnalysisUsingML.git ${projectDirectory}
fi

cd ${HOME}/${projectDirectory}


echo -e "create conda environment!!\nenv name: \"ecgWebAnalysisUsingML\""
conda env create -f requirements.yaml

echo "current Path: " ${PATH}
eval "$(conda shell.bash hook)"
#source ${HOME}/.bashrc
#source ${HOME}/anaconda3/etc/profile.d/conda.sh
#echo "current Path: " ${PATH}

echo "activate ecgWebAnalysisUsingML!!"
#conda init bash
conda activate ecgWebAnalysisUsingML

cd ${HOME}/${projectDirectory}/web
echo "current Path: " ${PATH}

echo "run gunicorn!!!"
gunicorn app:app
