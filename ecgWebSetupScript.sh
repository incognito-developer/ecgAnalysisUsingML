#!/bin/bash
#bash --version

if ps -f $$ | awk '{print $9}' | grep "bash"
then
   bash --version
else
    echo "Please run on bash shell!"
    ps -f $$
    echo "usage: bash filename.sh"
    exit 0
fi
   

projectDirectory=ecgWebAnalysisUsingML
echo "current PWD: " ${PWD}
echo "current Path: " ${PATH}

echo -e "\n\n"

echo -e "###Check the directory exists!!###\n"
if [ -d ${projectDirectory} ]
then
    echo "###" ${projectDirectory} "already exists!! Do you want to remove and download again?###"
    read -t 10 -p "(input \"yes\" to yes or wait 10 seconds)> " answer
    if [ ${answer} = "yes" ]
    then
	echo -e "\n\n###remove " ${HOME}/${projectDirectory} "###"
	rm -rf ${projectDirectory}
	echo -e "\n\n###Download the github repository!!###\n"
	git clone https://github.com/incognito-developer/ecgAnalysisUsingML.git ${projectDirectory}

    else
	echo -e "\n\n###pass remove directory and not download!!###\n\n"
    fi

else
    echo -e "\n\n###Download the github repository!!###\n"
    git clone https://github.com/incognito-developer/ecgAnalysisUsingML.git ${projectDirectory}
fi

cd ${HOME}/${projectDirectory}


echo -e "\n\n###create conda environment!!\nenv name: \"ecgWebAnalysisUsingML\"###"
conda env create -f requirements.yaml


echo -e "\n###current PWD: " ${PWD} "###"
echo "###current Path: " ${PATH} "###"
eval "$(conda shell.bash hook)"
#source ${HOME}/.bashrc
#source ${HOME}/anaconda3/etc/profile.d/conda.sh
#echo "current Path: " ${PATH}

echo -e "\n\n###activate ecgWebAnalysisUsingML!!###\n"
#conda init bash
conda activate ecgWebAnalysisUsingML

cd ${HOME}/${projectDirectory}/web/web
echo -e "\n\n###current PWD: " ${PWD} "###"
echo "###current Path: " ${PATH} "###"

echo -e "\n\n###run gunicorn!!!###"
gunicorn app:app
