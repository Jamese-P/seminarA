library ieee;
use ieee.std_logic_1164.all; 

entity d_flip_flop_w_reset is 
  port(clk, xrst, d: in std_logic;
       q, qb: out std_logic);
end d_flip_flop_w_reset;

architecture rtl of d_flip_flop_w_reset is 
  signal q1: std_logic;
begin
  q <= q1;
  qb <= not q1;
  process(clk, xrst)
  begin
    if(xrst = '0') then
      q1 <= '0';
    elsif(clk'event and clk = '1') then
      q1 <= d;
    end if;
  end process;
end rtl;
