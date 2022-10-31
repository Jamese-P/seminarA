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
	process (clk, xrst, button)
	begin
		state <= s0;
		if (xrst = '0') then
			state <= s0;
		end if;

		case state is
			when s0 =>
				count <= "000";
				sq4 <= "0000";
				sq3 <= "0000";
				sq2 <= "0000";
				sq1 <= "0000";
				if (button'event and button = '1') then
					state <= s1;
				end if;
			when s1 =>
				if (button'event and button = '0') then
					state <= s2;
				end if;
				if (clk'event and clk = '1') then
					count <= count + 1;
					if (count = "111") then
						sq1 <= sq1 + 1;
					end if;
					if (sq1 = "1001") then
						sq2 <= sq2 + 1;
					end if;
					if (sq2 = "1001") then
						sq3 <= sq3 + 1;
					end if;
					if (sq3 = "1001") then
						sq4 <= sq4 + 1;
					end if;
				end if;

			when s2 =>
				if (button'event and button = '1') then
					state <= s1;
				end if;

			when others =>
				state <= state;
		end case;

	end process;
	q4 <= sq4;
	q3 <= sq3;
	q2 <= sq2;
	q1 <= sq1;

end rtl;