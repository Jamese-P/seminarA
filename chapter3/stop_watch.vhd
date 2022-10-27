library ieee;  
use ieee.std_logic_1164.all;  

entity stop_watch is  
  port(clk, xrst: in std_logic;  
       button: in std_logic;
       q4, q3, q2, q1: out std_logic_vector(3 downto 0));
end stop_watch;  
  
architecture rtl of stop_watch is
  type state_type is (s0, s1, s2, s3);
  signal state: state_type;
begin
-- 記述開始


-- 記述終了
end rtl;
  
