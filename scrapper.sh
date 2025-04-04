page=$(curl -s https://www.fxempire.com/commodities/gold)
price=$(echo "$page" | grep -oP 'data-cy="instrument-price-value">[\d,\.]+' | grep -oP '[\d,\.]+')
price=$(echo "$price" | tr -d ',')
echo "$(date '+%Y-%m-%d %H:%M:%S'), $price" >> data.csv
