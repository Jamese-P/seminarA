library IEEE;
use IEEE.STD_LOGIC_1164.all;
-- use STD.TEXTIO.all;

entity tb_dividedby3FSM is
end;

architecture sim of tb_dividedby3FSM is
  component dividedby3FSM
    port (clk : in STD_LOGIC;
          rst : in STD_LOGIC;
          cnt : out STD_LOGIC_VECTOR (2 downto 0)
          );
  end component;

  signal clk, rst: STD_LOGIC;
  signal cnt : STD_LOGIC_VECTOR (2 downto 0);
begin
  dut: dividedby3FSM port map(clk, rst, cnt);
  process
  variable i : integer;
  begin
    for i in 0 to 20 loop
      clk <= '0'; wait for 5 ns;
      clk <= '1'; wait for 5 ns;
    end loop;
    wait;
  end process;

  process
  begin
    rst <= '1'; wait for 27 ns; rst <= '0';
    wait;
  end process;

end;
