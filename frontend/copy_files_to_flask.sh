USER=$1
HOST=$2

CSS_FILE=$(ls -tpr ./build/static/css/main.*.css | tail -n 1)
JS_FILE=$(ls -tpr ./build/static/js/main.*.js | tail -n 1)
JS_FILENAME=$(echo $JS_FILE | grep "main.*$" -o)
CSS_FILENAME=$(echo $CSS_FILE | grep "main.*$" -o)

cp $CSS_FILE $JS_FILE ../backend/static/
sed -i "" -e "s/main.*.js/$JS_FILENAME/" ../backend/templates/index.html
sed -i "" -E "s/main.*.css/$CSS_FILENAME/g" ../backend/templates/index.html

if [ -z "$USER" ] || [ -z "$$HOST" ]; then
  echo "no USER/HOST"
  exit 0
fi

scp ../backend/templates/index.html "$USER@$HOST:/home/$USER/pi-monitor/backend/templates/index.html"
scp -r ../backend/static "$USER@$HOST:/home/$USER/pi-monitor/backend"
