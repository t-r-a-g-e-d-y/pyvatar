#!/usr/bin/env bash
version=$(python3 --version 2>/dev/null | awk '{ gsub(/\./, "", $2) ; print $2 }')

if [ -z "$version" ] || [ "$version" -lt 360 ]; then
    echo "Requires Python 3.6 or newer"
    exit
fi

while getopts "i" o; do
    case ${o} in
        i )
            interactive=1
            ;;
    esac
done

gen_and_cat() { 
    python3 avatar.py > .avatar.txt && cat .avatar.txt
}

png_it() {
    python3 ansimg.py .avatar.txt output
}

if [ -n "$interactive" ]; then
    gen_and_cat
    while true; do
        read -rp "Save this avatar? (y/n) " yn
        case $yn in
            [yY]* )
                png_it && echo "Saved as output.png"
                rm .avatar.txt
                break
                ;;
            [nN]* )
                gen_and_cat
                ;;
            * )
                echo "Please answer yes or no."
                ;;
        esac
    done
else
    gen_and_cat
    png_it && echo "Saved as output.png"
    rm .avatar.txt
fi

