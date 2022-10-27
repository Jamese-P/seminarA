library ieee;  
use ieee.std_logic_1164.all;  

entity stop_watch_top is  
  port(CLOCK_50: in std_logic;
       RESET_N: in std_logic;
       KEY: in std_logic_vector(3 downto 0);
       HEX0, HEX1, HEX2, HEX3: out std_logic_vector(6 downto 0));
end stop_watch_top;

architecture testbench of stop_watch_top is
  signal xrst: std_logic;
  signal q1, q2, q3, q4: std_logic_vector(3 downto 0);
  component stop_watch is  
  port(clk, xrst: in std_logic;  
       button: in std_logic;
       q4, q3, q2, q1: out std_logic_vector(3 downto 0));
  end component;
  component seven_seg_decoder is
    port(clk: in std_logic;
         xrst: in std_logic;
         din: in  std_logic_vector(3 downto 0);
         dout: out std_logic_vector(6 downto 0));
  end component;
  for sw1: stop_watch use entity work.stop_watch(rtl);
begin
  sw1: stop_watch port map(clk => CLOCK_50, xrst => RESET_N, button => KEY(0), q1 => q1, q2 => q2, q3 => q3, q4 => q4);
  ssd1: seven_seg_decoder port map(clk => CLOCK_50, xrst => RESET_N, din => q4, dout => HEX3);
  ssd2: seven_seg_decoder port map(clk => CLOCK_50, xrst => RESET_N, din => q3, dout => HEX2);
  ssd3: seven_seg_decoder port map(clk => CLOCK_50, xrst => RESET_N, din => q2, dout => HEX1);
  ssd4: seven_seg_decoder port map(clk => CLOCK_50, xrst => RESET_N, din => q1, dout => HEX0);
end testbench;
