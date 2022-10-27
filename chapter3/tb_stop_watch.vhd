library ieee;  
use ieee.std_logic_1164.all;  

entity tb_stop_watch is  
end tb_stop_watch;

architecture testbench of tb_stop_watch is
  constant period: time := 10 ns;
  signal done: boolean := false;
  signal clk: std_logic := '0';
  signal xrst: std_logic := '1';
  signal button: std_logic;
  signal q1, q2, q3, q4: std_logic_vector(3 downto 0);
  component stop_watch is  
  port(clk, xrst: in std_logic;  
       button: in std_logic;
       q4, q3, q2, q1: out std_logic_vector(3 downto 0));
  end component;
  for sw1: stop_watch use entity work.stop_watch(rtl);
begin
  clock: process
  begin
    wait for period/2;
    if(done = false) then
      clk <= not clk;
    else
      assert (false) report "Simulation End!" severity failure;
    end if;
  end process;

  stim: process
  begin
    xrst <= '1';
    button <= '1';
    wait for period*2;
    wait for period/2;
    xrst <= '0';
    wait for period;
    xrst <= '1';
    wait for period*5;
    button <= '0';
    wait for period;
    button <= '1';
    wait for period*2222;
    button <= '0';
    wait for period;
    button <= '1';
    wait for period*500;
    button <= '0';
    wait for period;
    button <= '1';
    wait for period*500;
    xrst <= '0';
    wait for period;
    xrst <= '1';
    wait for period*5;
    button <= '0';
    wait for period;
    button <= '1';
    wait for period*11000;
    done <= true;
  end process;
    
  sw1: stop_watch port map(clk => clk, xrst => xrst, button => button, q1 => q1, q2 => q2, q3 => q3, q4 => q4);
end testbench;
