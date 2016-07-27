
% Steps to get t-SNE
% replace first comma with '|' in all rows, including the header
% regexprep('S0017,S0023,0.06752825465919876','^(SS?\d+),','$1|')

% A = ReadCSV('public-adhoc-Jaccard.csv');
A = ReadCSV('public-adhoc-BC_full.csv');

[r,c,v] = find(A);
[r1,r2] = SplitStr(r,'|');
C = Assoc(r1,r2,v);
D = Adj(C);
[i,j,x] = find(D);
[m,n] = size(D);
vm = Str2mat(v);
for c = 1:numel(x)
	x(c) = str2num(vm(x(c),:));
end
D = sparse(i,j,x,m,n);
D = full(D);
D = [zeros(size(D,1),1) D; 0 zeros(1,size(D,2))];
D = D + D.';

X = tsne_d(D, [], 2, 2.5);
plot(X(:,1),X(:,2),'o')
Cr = Row(C);
Cc = Col(C);
l = num2cell(Str2mat([ Cr StrSubind(Cc, NumStr(Cc)) ]),2);
l = cellfun(@deblank, l,'UniformOutput',false);

text(X(:,1),X(:,2),l)



fid = fopen('t-SNE-BC-50-perp-2.5.csv','w');
fprintf(fid,'sampleid,x,y\n');
for i = 1:size(X,1)
	fprintf(fid,'%s%f,%f\n',deblank(l{i}),X(i,1),X(i,2));
end
fclose(fid);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ct = 'jet'; % 'jet'
dims = [0 0 15 9];
figure; scatter(x,y,40,lon,'filled'); title('t-SNE BC 50x50 perp 2.5, color by longitude (deg E)'); colorbar; colormap(ct); text(x+10,y,Library); savefig('tsne-lon'); fig = gcf; fig.PaperUnits = 'inches'; fig.PaperPosition = dims; print('tsne-lon','-dpng', '-r0');
figure; scatter(x,y,40,lat,'filled'); title('t-SNE BC 50x50 perp 2.5, color by latitude (deg N)'); colorbar; colormap(ct); text(x+10,y,Library); savefig('tsne-lat'); fig = gcf; fig.PaperUnits = 'inches'; fig.PaperPosition = dims; print('tsne-lat','-dpng', '-r0');
figure; scatter(x,y,40,pressure,'filled'); title('t-SNE BC 50x50 perp 2.5, color by pressure (dbar)'); colorbar; colormap(ct); text(x+10,y,Library); savefig('tsne-pressure'); fig = gcf; fig.PaperUnits = 'inches'; fig.PaperPosition = dims; print('tsne-pressure','-dpng', '-r0');
figure; scatter(x,y,40,depth,'filled'); title('t-SNE BC 50x50 perp 2.5, color by depth (m)'); colorbar; colormap(ct); text(x+10,y,Library); savefig('tsne-depth'); fig = gcf; fig.PaperUnits = 'inches'; fig.PaperPosition = dims; print('tsne-depth','-dpng', '-r0');
figure; scatter(x,y,40,temp,'filled'); title('t-SNE BC 50x50 perp 2.5, color by temperature (deg C)'); colorbar; colormap(ct); text(x+10,y,Library); savefig('tsne-temp'); fig = gcf; fig.PaperUnits = 'inches'; fig.PaperPosition = dims; print('tsne-temp','-dpng', '-r0');
figure; scatter(x,y,40,sal,'filled'); title('t-SNE BC 50x50 perp 2.5, color by salinity (pss-78)'); colorbar; colormap(ct); text(x+10,y,Library); savefig('tsne-sal'); fig = gcf; fig.PaperUnits = 'inches'; fig.PaperPosition = dims; print('tsne-sal','-dpng', '-r0');


figure; semilogx(norm_cnt, cnt_norm_cnt/1189585624, 'o', norm_cnt_3, cnt_norm_cnt_3/985637920, '+', norm_cnt_4, cnt_norm_cnt_4/903513026, '*');
legend('S0002','S0003','S0004'); xlabel('log(normalized abundance)'); ylabel('normalized frequency'); title('frequency of normalized relative kmer abundances, k=11');

figure; semilogx(norm_cnt, cnt_norm_cnt, 'o', norm_cnt_3, cnt_norm_cnt_3, '+', norm_cnt_4, cnt_norm_cnt_4, '*');
legend('S0002','S0003','S0004'); xlabel('log(normalized abundance)'); ylabel('frequency'); title('frequency of normalized relative kmer abundances, k=11');

figure; semilogx(norm_cnt, cnt_norm_cnt, 'o');
legend('Srand01'); xlabel('log(normalized abundance)'); ylabel('frequency'); title('frequency of normalized relative kmer abundances of a Random Sequence, GC prob.=0.417, k=11');

figure; semilogx(norm_cnt, cnt_norm_cnt, 'o', norm_cnt_3, cnt_norm_cnt_3, '+', norm_cnt_4, cnt_norm_cnt_4, '*', norm_cntr, cnt_norm_cntr, 'x');
legend('S0002','S0003','S0004','Srand01'); xlabel('log(normalized abundance)'); ylabel('frequency'); title('frequency of normalized relative kmer abundances, k=11');

figure; semilogx(norm_cnt, cnt_norm_cnt/1189585624, 'o', norm_cnt_3, cnt_norm_cnt_3/985637920, '+', norm_cnt_4, cnt_norm_cnt_4/903513026, '*', norm_cntr, cnt_norm_cntr/963323535, 'x');
legend('S0002','S0003','S0004','Srand01'); xlabel('log(normalized abundance)'); ylabel('normalized frequency'); title('frequency of normalized relative kmer abundances, k=11');

figure; semilogx(norm_cnt, cnt_norm_cnt/1189585624, 'o', norm_cnt_3, cnt_norm_cnt_3/985637920, '+', norm_cnt_4, cnt_norm_cnt_4/903513026, '*', norm_cntr, cnt_norm_cntr/963323535, 'x', norm_cntr2, cnt_norm_cntr2/963323535, 'd');
legend('S0002','S0003','S0004','Srand01','Srand02'); xlabel('log(normalized abundance)'); ylabel('normalized frequency'); title('frequency of normalized relative kmer abundances, k=11');



figure; scatter(norm_cnt, sum_ct); xlabel('Peak relative abundance'); ylabel('Total number of kmers'); text(norm_cnt, sum_ct, num2str(Library));
figure; scatter(EntropySkew50, sum_ct); xlabel('Entropy Skew'); ylabel('Total number of kmers'); text(EntropySkew50, sum_ct, num2str(Library));
figure; scatter(Simpsondiversity50, norm_cnt); xlabel('Simpson diversity'); ylabel('Peak relative abundance'); text(Simpsondiversity50, norm_cnt, num2str(Library));
figure; scatter(EntropySkew50, norm_cnt); xlabel('Entropy Skew'); ylabel('Peak relative abundance'); text(EntropySkew50, norm_cnt, num2str(Library));

