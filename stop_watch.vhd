library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity stop_watch is
	port (
		clk, xrst : in std_logic;
		button : in std_logic;
		q4, q3, q2, q1 : out std_logic_vector(3 downto 0));
end stop_watch;

architecture rtl of stop_watch is
	type state_type is (s0, s1, s2, s3);
	signal state : state_type;
	signal count : std_logic_vector(2 downto 0);
	signal sq1, sq2, sq3, sq4 : std_logic_vector(3 downto 0);
begin
	process (xrst)
	begin
		if (xrst = '0') then
			state <= s0;
		end if;
	end process;

	process (clk, button)
	begin

		case state is
			when s0 =>
				if (button = '0') then
					state <= s1;
				else
					state <= state;
				end if;
			when s1 =>
				if (button = '0') then
					state <= s2;
				else
					state <= state;
				end if;
			when s2 =>
				if (button = '0') then
					state <= s1;
				else
					state <= state;
				end if;
			when others =>
				state <= state;
		end case;
	end process;

	process (clk)
	begin
		if (state = s0) then
			count <= "000";
			sq4 <= "0000";
			sq3 <= "0000";
			sq2 <= "0000";
			sq1 <= "0000";
		elsif (state = s1) then
			if (clk'event and clk = '1') then
				count <= count + 1;
				if (count = "111") then
					sq1 <= sq1 + 1;
					count <= "000";
				end if;
				if (sq1 = "1010") then
					sq2 <= sq2 + 1;
					sq1 <= "0000";
				end if;
				if (sq2 = "1010") then
					sq3 <= sq3 + 1;
					sq2 <= "0000";
				end if;
				if (sq3 = "1010") then
					sq4 <= sq4 + 1;
					sq3 <= "0000";
				end if;

			end if;
		end if;
	end process;

	process (clk)
	begin
		q4 <= sq4;
		q3 <= sq3;
		q2 <= sq2;
		q1 <= sq1;
	end process;

end rtl;