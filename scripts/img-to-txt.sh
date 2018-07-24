for file in $(ls gs_output/); do 
    tesseract gs_output/$file ts_output/$file
done
