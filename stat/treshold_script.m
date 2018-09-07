% This script find threshold of a matrix

threshold = (2*10^4);

fileID = fopen('n_packets_week1','r');
formatSpec = '%d';
A = fscanf(fileID, formatSpec);
A = transpose(A);
indices = find(A > threshold);
A(indices) = [];

disp(length(indices));
disp(length(A));