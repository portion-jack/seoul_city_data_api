if (source seoul_api/bin/activate) ; then
    source seoul_api/bin/activate
    echo "venv activated"

    python _seoul_api.py
    
    git add .
    git commit -m "`date '+%Y-%m-%d'`"
    git push origin main
else
    echo "conda should be activated"
fi

