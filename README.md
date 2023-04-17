# HaThermos

Command to install python lib :
```bash
pip install -r requirements.txt
```
To modify the CSS, you need to install TailwindCSS. You can do this by running the following command:

```bash
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.3.1/tailwindcss-linux-x64 && chmod +x tailwindcss-linux-x64 && mv tailwindcss-linux-x64 tailwindcss
```


```bash
./tailwindcss -i ./static/css/input.css -o ./static/css/tailwind.css --watch
```