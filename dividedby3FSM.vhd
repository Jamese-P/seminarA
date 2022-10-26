library IEEE; use IEEE.STD_LOGIC_1164.all;

entity dividedby3FSM is 
  port(clk, rst: in STD_LOGIC;
       cnt: out STD_LOGIC_VECTOR(2 downto 0));
end;

architecture synth of dividedby3FSM is
 type statetype is (S0, S1, S2);
 signal state, nextstate: statetype;

begin
  process(clk, rst) begin
    if (rst='1') then state <= S0;
    elsif rising_edge(clk) then
      state <= nextstate;
    end if;
  end process;

  nextstate <= S1 when state = S0 else
               S2 when state = S1 else
               S0;

  cnt <= "001" when state = S0 else "000";
end;
 