library IEEE;
use IEEE.STD_LOGIC_1164.all;
use STD.TEXTIO.all;

entity tb_and3 is
end;
architecture sim of tb_and3 is
  component and3
    port(a: in  STD_LOGIC_VECTOR(2 downto 0);
             y: out STD_LOGIC);
  end component;
  signal a: STD_LOGIC_VECTOR(2 downto 0);
  signal y, clk, reset: STD_LOGIC;
  signal yexpected: STD_LOGIC;
  constant MEMSIZE: integer := 10000;
  type tvarray is array(MEMSIZE downto 0) of
    STD_LOGIC_VECTOR(3 downto 0);
  signal testvectors: tvarray;
  shared variable vectornum, errors: integer;
begin
  dut: and3 port map(a, y);
  process
  begin
    clk <= '1'; wait for 5 ns;
    clk <= '0'; wait for 5 ns;
  end process;

  process is
    file tv: TEXT;
    variable i, j: integer;
    variable L: line;
    variable ch: character;
  begin
    i := 0;
    FILE_OPEN(tv, "and3.tv", READ_MODE);
    while not endfile(tv) loop
      readline(tv, L);
      for j in 3 downto 0 loop
        read(L, ch);
        if (ch = '_') then read(L, ch);
        end if;
        if (ch = '0') then
          testvectors(i)(j) <= '0';
        else testvectors(i)(j) <= '1';
    end if;
      end loop;
      i := i + 1;
    end loop;
    vectornum := 0; errors := 0;
    reset <= '1'; wait for 27 ns; reset <= '0';
    wait;
  end process;

  process (clk)
  begin
    if (clk'event and clk = '1') then
      a <= testvectors(vectornum)(3 downto 1)
           after 1 ns;
      yexpected <= testvectors(vectornum)(0)
                   after 1 ns;
    end if;
  end process;

  process (clk)
  begin
    if (clk'event and clk = '0' and reset = '0') then
      assert y = yexpected
        report "Error: y = " & STD_LOGIC'image(y);
      if (y /= yexpected) then
        errors := errors + 1;
      end if;
      vectornum := vectornum + 1;
      if (is_x(testvectors(vectornum))) then
        if (errors = 0) then
          report "Just kidding -- " &
            integer'image(vectornum) &
            " tests completed successfully."
            severity failure;
        else
          report integer'image(vectornum) &
            " tests completed, errors = " &
            integer'image(errors)
            severity failure;
        end if;
      end if;
    end if;
  end process;
end;
