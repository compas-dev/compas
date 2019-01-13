%---------------------------------------------------------------------
%  This is the file beam1.m.  Version April 2007.
%  Written by Krister Svanberg <krille@math.kth.se>.
%  It calculates function values (but no gradients)
%  for the "beam problem" from the MMA paper.
%
%    minimize 0.0624*(x(1) + x(2) + x(3) + x(4) + x(5))
%  subject to 61/(x(1)^3) + 37/(x(2)^3) + 19/(x(3)^3) +
%              7/(x(4)^3) +  1/(x(5)^3) =< 1,
%              1 =< x(j) =< 10, for j=1,..,5.
%  (the bounds on x(j) are defined in gcbeaminit.m)
%
function [f0val,fval] = beam1(xval);
%
nx = 5;
eeen = ones(nx,1);
c1 = 0.0624;
c2 = 1;
aaa = [61 37 19 7 1]';
xval2 = xval.*xval;
xval3 = xval2.*xval;
xinv3 = eeen./xval3;
f0val=c1*eeen'*xval;
fval = aaa'*xinv3-c2;
%---------------------------------------------------------------------


