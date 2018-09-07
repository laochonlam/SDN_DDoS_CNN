%% data reading
capture = dir('../raw_data/data_normal/07*');
% capture = dir('data/07*');
numcapture = length(capture);
mydata = cell(1, numcapture);
filename = {capture.name};

Normal_featureMat = zeros(numcapture, 31);

for k = 1:numcapture
    pathname = strcat('../raw_data/data_normal/', filename{k});
    fileID = fopen(pathname,'r');
    formatSpec = '%f';
    C = fscanf(fileID, formatSpec);
    C = transpose(C);
    Normal_featureMat(k,:) = C;
    fclose(fileID);
end

%% data reading
capture = dir('../raw_data/data_abnormal/07*');
% capture = dir('data/07*');
numcapture = length(capture);
mydata = cell(1, numcapture);
filename = {capture.name};

Abnormal_featureMat = zeros(numcapture, 31);

for k = 1:numcapture
    pathname = strcat('../raw_data/data_abnormal/', filename{k});
    fileID = fopen(pathname,'r');
    formatSpec = '%f';
    C = fscanf(fileID, formatSpec);
    C = transpose(C);
    Abnormal_featureMat(k,:) = C;
    fclose(fileID);
end


%% data processing

% % 1Packet_count_total
% figure
% plot(Normal_featureMat(:,1), 'b.'); hold on;
% plot(Abnormal_featureMat(:,1), 'r.'); hold off;
% xlim([0 6000]); 
% xlabel('Num of samples');
% ylabel('Num of packets');

% % 2Packet_count_interval
% figure
% plot(Normal_featureMat(:,2), 'b.'); hold on;
% plot(Abnormal_featureMat(:,2), 'r.'); hold off;
% xlim([0 6000]); 
% xlabel('Num of samples');
% ylabel('Num of packets');

% % 3Packet count ratio
% figure
% plot(Normal_featureMat(:, 3), 'b.'); hold on;
% plot(Abnormal_featureMat(:, 3), 'r.'); hold off;
% xlim([0 6000]);  ylim([0, 0.6]);
% xlabel('Num of samples');
% ylabel('Ratio');

% % 4mean of all packet count
% figure
% plot(Normal_featureMat(:,4), 'b.'); hold on;
% plot(Abnormal_featureMat(:,4), 'r.'); hold off;
% xlim([0 6000]); ylim([0 10000]); 
% xlabel('Num of samples');
% ylabel('Mean');

% % 5mean of interval packet count
% figure
% plot(Normal_featureMat(:,5), 'b.'); hold on;
% plot(Abnormal_featureMat(:,5), 'r.'); hold off;
% xlim([0 6000]); ylim([0 40])
% xlabel('Num of samples');
% ylabel('Mean');

% % 6packet_mean_ratio
% figure
% plot(Normal_featureMat(:,6), 'b.'); hold on;
% plot(Abnormal_featureMat(:,6), 'r.'); hold off;
% xlim([0 6000]); 
% ylim([0 8]);
% xlabel('Num of Samples');
% ylabel('Ratio');

% % 7packet_mean_relative_distance
% figure
% plot(Normal_featureMat(:,7), 'b.'); hold on;
% plot(Abnormal_featureMat(:,7), 'r.'); hold off;
% xlim([0 6000]); 
% ylim([0 8000]);
% xlabel('Num of samples');
% ylabel('Relative Distance');


% % 8median of all packet count
% figure
% plot(Normal_featureMat(:,8), 'b.'); hold on;
% plot(Abnormal_featureMat(:,8), 'r.'); hold off;
% xlim([0 6000]);
% xlabel('Num of samples');
% ylabel('Median');

% % 9median of interval packet count
% figure
% plot(Normal_featureMat(:,9), 'b.'); hold on;
% plot(Abnormal_featureMat(:,9), 'r.'); hold off;
% xlim([0 6000]); ylim([0 20]); 
% xlabel('Num of samples');
% ylabel('Median');

% % 10packet_median_ratio
% figure
% plot(Normal_featureMat(:,10), 'b.'); hold on;
% plot(Abnormal_featureMat(:,10), 'r.'); hold off;
% xlim([0 6000]); 
% ylim([0 12]);
% xlabel('Num of Samples');
% ylabel('Ratio');

% % 11packet_median_relative_distance
% figure
% plot(Normal_featureMat(:,11), 'b.'); hold on;
% plot(Abnormal_featureMat(:,11), 'r.'); hold off;
% xlim([0 6000]); 
% ylim([0 16]);
% xlabel('Num of samples');
% ylabel('Relative Distance');


% 12mean_of_all_bytes_count
% figure
% plot(Normal_featureMat(:,12), 'b.'); hold on;
% plot(Abnormal_featureMat(:,12), 'r.'); hold off;
% xlim([0 6000]);
% xlabel('Num of samples');
% ylabel('Mean');

% % 13mean_of_interval_bytes_count
% figure
% plot(Normal_featureMat(:,13), 'b.'); hold on;
% plot(Abnormal_featureMat(:,13), 'r.'); hold off;
% xlim([0 6000]); ylim([0 15000])
% xlabel('Num of samples');
% ylabel('Mean');

% % 14bytes_mean_ratio
% figure
% plot(Normal_featureMat(:,14), 'b.'); hold on;
% plot(Abnormal_featureMat(:,14), 'r.'); hold off;
% xlim([0 6000]); 
% ylim([0 10]);
% xlabel('Num of Samples');
% ylabel('Ratio');

% % 15bytes_mean_relative_distance
% figure
% plot(Normal_featureMat(:,15), 'b.'); hold on;
% plot(Abnormal_featureMat(:,15), 'r.'); hold off;
% xlim([0 6000]); 
% ylim([0 4000000]);
% xlabel('Num of samples');
% ylabel('Relative Distance');

% % 16median_of_all_bytes_count
% figure
% plot(Normal_featureMat(:,16), 'b.'); hold on;
% plot(Abnormal_featureMat(:,16), 'r.'); hold off;
% xlim([0 6000]);
% xlabel('Num of samples');
% ylabel('Median');

% % 17median_of_interval_bytes_count
% figure
% plot(Normal_featureMat(:,17), 'b.'); hold on;
% plot(Abnormal_featureMat(:,17), 'r.'); hold off;
% xlim([0 6000]); ylim([0 20000])
% xlabel('Num of samples');
% ylabel('Median');

% % 18packet_median_ratio
% figure
% plot(Normal_featureMat(:,18), 'b.'); hold on;
% plot(Abnormal_featureMat(:,18), 'r.'); hold off;
% xlim([0 6000]); 
% ylim([0 50]);
% xlabel('Num of Samples');
% ylabel('Ratio');

% % 19packet_median_relative_distance
% figure
% plot(Normal_featureMat(:,19), 'b.'); hold on;
% plot(Abnormal_featureMat(:,19), 'r.'); hold off;
% xlim([0 6000]); 
% ylim([0 20000]);
% xlabel('Num of samples');
% ylabel('Relative Distance');

% % 20pair_flow_all
% figure
% plot(Normal_featureMat(:,20), 'b.'); hold on;
% plot(Abnormal_featureMat(:,20), 'r.'); hold off;
% xlim([0 6000]); 
% % ylim([0 20000]);
% xlabel('Num of samples');
% ylabel('Num of Pair-flow');

% % 21flow_all
% figure
% plot(Normal_featureMat(:,21), 'b.'); hold on;
% plot(Abnormal_featureMat(:,21), 'r.'); hold off;
% xlim([0 6000]); 
% % ylim([0 20000]);
% xlabel('Num of samples');
% ylabel('Num of Flows');

% % 22pair_flow_interval
% figure
% plot(Normal_featureMat(:,22), 'b.'); hold on;
% plot(Abnormal_featureMat(:,22), 'r.'); hold off;
% xlim([0 6000]);     
% % ylim([0 20000]);
% xlabel('Num of samples');
% ylabel('Num of Pair-flow');
% 
% % 23flow_interval
% figure
% plot(Normal_featureMat(:,23), 'b.'); hold on;
% plot(Abnormal_featureMat(:,23), 'r.'); hold off;
% xlim([0 6000]); 
% % ylim([0 20000]);
% xlabel('Num of samples');
% ylabel('Num of Flows');

% % 24PPf_all
% figure
% plot(Normal_featureMat(:,24), 'b.'); hold on;
% plot(Abnormal_featureMat(:,24), 'r.'); hold off;
% xlim([0 6000]);     
% % ylim([0 20000]);
% xlabel('Num of samples');
% ylabel('PPf');

% % 25PPf_interval
% figure
% plot(Normal_featureMat(:,25), 'b.'); hold on;
% plot(Abnormal_featureMat(:,25), 'r.'); hold off;
% xlim([0 6000]); 
% % ylim([0 20000]);
% xlabel('Num of samples');
% ylabel('PPf');

% % 26pair_flow_ratio
% figure
% plot(Abnormal_featureMat(:,26), 'r.'); hold on;
% plot(Normal_featureMat(:,26), 'b.'); hold off;
% 
% xlim([0 6000]); 
% ylim([0 50]);
% xlabel('Num of Samples');
% ylabel('Ratio');

% 27pair_flow_relative_distance
% figure
% plot(Normal_featureMat(:,27), 'b.'); hold on;
% plot(Abnormal_featureMat(:,27), 'r.'); hold off;
% xlim([0 6000]); 
% % ylim([0 20000]);
% xlabel('Num of samples');
% ylabel('Relative Distance');

% % 28entropy_all
% figure
% plot(Normal_featureMat(:,28), 'b.'); hold on;
% plot(Abnormal_featureMat(:,28), 'r.'); hold off;
% xlim([0 6000]); 
% xlabel('Num of samples');
% ylabel('Entropy');

% % 29entropy_interval
% figure
% plot(Normal_featureMat(:,29), 'b.'); hold on;
% plot(Abnormal_featureMat(:,29), 'r.'); hold off;
% xlim([0 6000]); 
% xlabel('Num of samples');
% ylabel('Entropy');


% % 30entropy_ratio
% figure
% plot(Abnormal_featureMat(:,30), 'b.'); hold on;
% plot(Normal_featureMat(:,30), 'r.'); hold off;
% xlim([0 6000]); ylim([0 20]) 
% xlabel('Num of Samples');
% ylabel('Ratio');

% % % 31entropy_relative_distance
% figure
% plot(Normal_featureMat(:,31), 'b.'); hold on;
% plot(Abnormal_featureMat(:,31), 'r.'); hold off;
% xlim([0 6000]); 
% % ylim([0 8000]);
% xlabel('Num of samples');
% ylabel('Relative Distance');
