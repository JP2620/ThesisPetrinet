PATH_INPUTS="division_de_red"
PATH_OUTPUT="division_de_red/salida"
PATH_OUTPUT_RELATIVE="salida"
rm "${PATH_OUTPUT}"/*.json "${PATH_OUTPUT}"/*.dot "${PATH_OUTPUT}"/*.png
cd "${PATH_INPUTS}"
python ./algoritmo.py
python ./graficador.py "${PATH_OUTPUT_RELATIVE}"/mincov_filled_out_final.json "${PATH_OUTPUT_RELATIVE}"/mincov_out_.json.json
gwenview "${PATH_OUTPUT_RELATIVE}"//grid_image.png 