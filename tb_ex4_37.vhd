library IEEE;
use IEEE.STD_LOGIC_1164.all;
-- use STD.TEXTIO.all;

entity tb_ex4_37 is
end;

architecture sim of tb_ex4_37 is
  component ex4_37
    port (clk : in STD_LOGIC;
          rst : in STD_LOGIC;
          cnt : out STD_LOGIC_VECTOR (2 downto 0)
          );
  end component;

  signal clk, rst: STD_LOGIC;
  signal cnt : STD_LOGIC_VECTOR (2 downto 0);
 
begin
  dut: ex4_37 port map(clk, rst, cnt);
  process
  variable i: integer;
  begin
    for i in 0 to 20 loop
      clk <= '0'; wait for 5 ns;
      clk <= '1'; wait for 5 ns;
    end loop;
    wait;
  end process;

  process is
  begin
    rst <= '1'; wait for 19 ns; rst <= '0';
    wait;
  end process;
end;
