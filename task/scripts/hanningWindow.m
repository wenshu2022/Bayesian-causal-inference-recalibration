function w = hanningWindow(n)

%HANNINGWINDOW   Hanning window.
%
%   HANNING(N) returns the N-point symmetric Hanning window in a column
%   vector.  Note that the first and last zero-weighted window samples
%   are not included.
%
%   This is an adaptation of the function 'HANNING' in the Signal
%   Processing toolbox - Made by David Meijer on 8-10-2015.

% I only support symmetric Hanning windows
w = sym_hanning(n);

%---------------------------------------------------------------------
function w = sym_hanning(n)
%SYM_HANNING   Symmetric Hanning window. 
%   SYM_HANNING Returns an exactly symmetric N point window by evaluating
%   the first half and then flipping the same samples over the other half.

if ~rem(n,2)
   % Even length window
   half = n/2;
   w = calc_hanning(half,n);
   w = [w; w(end:-1:1)];
else
   % Odd length window
   half = (n+1)/2;
   w = calc_hanning(half,n);
   w = [w; w(end-1:-1:1)];
end

%---------------------------------------------------------------------
function w = calc_hanning(m,n)
%CALC_HANNING   Calculates Hanning window samples.
%   CALC_HANNING Calculates and returns the first M points of an N point
%   Hanning window.

w = .5*(1 - cos(2*pi*(1:m)'/(n+1))); 

% [EOF]