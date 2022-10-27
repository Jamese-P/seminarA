library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity tx is
  generic(N: integer := 32;
          K: integer := 4;
          W: integer := 3);
  port(
    CLOCK_50, RESET_N: in std_logic;
    -- KEY(0): start button
    -- KEY(2): write enable
    -- KEY(3): address increment
    KEY: in std_logic_vector(3 downto 0);
    -- SW(9 downto 8): mode
    -- SW(3 downto 0): din
    SW: in std_logic_vector(9 downto 0);
    -- GPIO_1(3 downto 0): data bits
    -- GPIO_1(4): start bit
    -- GPIO_1(5): ready bit
    GPIO_1: inout std_logic_vector (35 downto 0);
    -- LEDR: for debug
    LEDR: out std_logic_vector (9 downto 0);
    HEX0, HEX1, HEX2, HEX3, HEX4, HEX5: out std_logic_vector(6 downto 0));
end tx;

architecture rtl of tx is
  constant cnt_max: std_logic_vector(31 downto 0):= X"000003FF";
  type state_type is (s0, s1, s2, s3);
  signal state: state_type;
  signal sout: std_logic_vector (3 downto 0);
  signal clk, xrst: std_logic;
  signal enable: std_logic;
  signal clk_tx: std_logic;
  signal start: std_logic;
  signal ready: std_logic;
  signal we: std_logic;
  signal wadr, radr: std_logic_vector (2 downto 0);
  signal din, dout: std_logic_vector (3 downto 0);
  signal debug0, debug1, debug2: std_logic_vector (3 downto 0);
  -- 送信用クロック生成回路
  component clock_gen
    generic(N: integer);
    port(clk, xrst: in std_logic;
         enable: in std_logic;
         cnt_max: in std_logic_vector (N-1 downto 0);
         clk_tx: out std_logic);
  end component;
  -- Kビット・Wワードの RAM
  component ram_WxK
    generic(K: integer;
            W: integer);
    port(clk: in std_logic;
         din: in std_logic_vector (K-1 downto 0);
         wadr: in std_logic_vector (W-1 downto 0);
         radr: in std_logic_vector (W-1 downto 0);
         we: in std_logic;
         dout: out std_logic_vector (K-1 downto 0));
  end component;
  -- 7セグメントデコーダ
  component seven_seg_decoder is
    port(clk: in std_logic;
         xrst: in std_logic;
         din: in std_logic_vector(3 downto 0);
         dout: out std_logic_vector(6 downto 0));
  end component;
begin
  clk <= CLOCK_50;
  xrst <= RESET_N;
  din <= SW(3 downto 0);
  ready <= GPIO_1(5);
  we <= not KEY(2);

  cg1: clock_gen generic map(N => N) port map(clk => clk, xrst => xrst, enable => enable, cnt_max => cnt_max, clk_tx => clk_tx);
  ram1: ram_WxK generic map(K => K, W => W) port map(clk => clk, din => din, wadr => wadr, radr => radr, we => we, dout => dout);
-- 記述開始


-- 記述終了
end rtl;

