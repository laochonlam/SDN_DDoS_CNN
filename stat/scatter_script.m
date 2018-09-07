% This script is use for plot 

%% n_packets
fileID = fopen('n_packets_week1','r');
formatSpec = '%d';
A = fscanf(fileID, formatSpec);
A = transpose(A);
% threshold = (150);
% indices = find(A > threshold);
% A(indices) = [];

fileID = fopen('n_packets_week2','r');
formatSpec = '%d';
B = fscanf(fileID, formatSpec);
B = transpose(B);

%% n_bytes
fileID = fopen('n_bytes_week1','r');
formatSpec = '%d';
C = fscanf(fileID, formatSpec);
C = transpose(C);

fileID = fopen('n_bytes_week2','r');
formatSpec = '%d';
D = fscanf(fileID, formatSpec);
D = transpose(D);

%% plot 

figure;
y = linspace(1, length(A), length(A));
npacketsw1 = subplot(2, 2, 1);
scatter(npacketsw1, y, A);
title("week1: n\_packets");
xlabel("number");
ylabel("value");

y = linspace(1, length(B), length(B));
npacketsw2 = subplot(2, 2, 2);
scatter(npacketsw2, y, B);
title("week2: n\_packets");
xlabel("number");
ylabel("value");

y = linspace(1, length(C), length(C));
nbytesw1 = subplot(2, 2, 3);
scatter(nbytesw1, y, C);
title("week1: n\_bytes");
xlabel("number");
ylabel("value");

y = linspace(1, length(D), length(D));
nbytesw2 = subplot(2, 2, 4);
scatter(nbytesw2, y, D);
title("week1: n\_bytes");
xlabel("number");
ylabel("value");


disp(mean(A));
disp(mean(B));
disp(mean(C));
disp(mean(D));
