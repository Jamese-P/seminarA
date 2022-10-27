library IEEE; use IEEE.STD_LOGIC_1164.all;

entity and3 is 
  port(a: in STD_LOGIC_VECTOR(2 downto 0);
       y: out STD_LOGIC);
end;

architecture synth of and3 is
begin
  y <= a(2) and a(1) and a(0);
end;
