set yrange [0:400]
set ylabel "Values"
set xlabel "Time"
plot "./Cupboard_2okt_2.txt" title "Cupboard", "./Room_2okt_50k.txt" title "Study", ".//2okt_Living_room_50k_2.txt" title "Living room", "./Computer_Case_2okt.txt" title "Computer Case"
