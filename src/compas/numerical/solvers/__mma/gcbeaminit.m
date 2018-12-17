%---------------------------------------------------------------------
%  This is the file gcbeaminit.m.  Version April 2007.
%  Written by Krister Svanberg <krille@math.kth.se>.
%  Some parameters and the starting point are defined
%  for the "beam problem" from the MMA paper.
%
%    minimize 0.0624*(x(1) + x(2) + x(3) + x(4) + x(5))
%  subject to 61/(x(1)^3) + 37/(x(2)^3) + 19/(x(3)^3) +
%              7/(x(4)^3) +  1/(x(5)^3) =< 1,
%              1 =< x(j) =< 10, for j=1,..,5.
%
m = 1;
n = 5;
epsimin = 0.0000001;
eeen    = ones(n,1);
eeem    = ones(m,1);
zeron   = zeros(n,1);
zerom   = zeros(m,1);
xval    = 5*eeen;
xold1   = xval;
xold2   = xval;
xmin    = eeen;
xmax    = 10*eeen;
low     = xmin;
upp     = xmax;
c       = 1000*eeem;
d       = eeem;
a0      = 1;
a       = zerom;
raa0    = 0.01;
raa     = 0.01*eeem;
raa0eps = 0.000001;
raaeps  = 0.000001*eeem;
outeriter = 0;
maxoutit  = 1;
kkttol  = 0;
%
%---------------------------------------------------------------------
