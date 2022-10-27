library IEEE; use IEEE.STD_LOGIC_1164.all;

entity ex4_37 is 
  port(clk, rst: in STD_LOGIC;
       cnt: out STD_LOGIC_VECTOR(2 downto 0));
end;

architecture synth of ex4_37 is
 type statetype is (S0, S1, S2, S3, S4, S5, S6, S7);
 signal state, nextstate: statetype;

begin
  process(clk, rst) begin
    if (rst='1') then state <= S0;
    elsif rising_edge(clk) then
      state <= nextstate;
    end if;
  end process;

  nextstate <= S7 when state = S6 else
		S6 when state = S5 else
		S5 when state = S4 else
		S4 when state = S3 else
		S3 when state = S2 else
		S2 when state = S1 else
               S1 when state = S0 else
               S0;

  cnt <= "100" when state = S7 else
	"101" when state = S6 else
	"111" when state = S5 else
	"110" when state = S4 else
	"010" when state = S3 else
	"011" when state = S2 else
	"001" when state = S1 else
	"000";
end;
