
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

