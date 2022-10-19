library ieee;                           -- ライブラリの指定
use ieee.std_logic_1164.all;            -- 基本関数の呼出し

entity async_octal_counter is
  -- port：入出力信号線の宣言
  -- std_logic：1ビット信号線
  -- std_logic_vector：多ビット信号線
  port(clk, xrst: in std_logic;  
       q: out std_logic_vector(2 downto 0));
end async_octal_counter;

architecture gate_level of async_octal_counter is
  -- signal：回路内部で使用する信号線の宣言
  signal d1, d2, d3, q1, q2, q3, qb1, qb2, qb3: std_logic;
  -- component：回路内部で使用する回路要素の宣言
  -- 今回は D フリップフロップを回路要素として宣言
  component d_flip_flop_w_reset
    port(clk, xrst, d: in std_logic;  
         q, qb: out std_logic);
  end component;  
begin
  -- Dフリップフロップ 3つをインスタンス化
  -- port map：Dフリップフロップの入出力信号と本回路の内部信号もしくは入出力信号を接続
  dff1: d_flip_flop_w_reset port map(clk => clk, xrst => xrst, d => d1, q => q1, qb => qb1);
  dff2: d_flip_flop_w_reset port map(clk => clk, xrst => xrst, d => d2, q => q2, qb => qb2);
  dff3: d_flip_flop_w_reset port map(clk => clk, xrst => xrst, d => d3, q => q3, qb => qb3);
-- ゲートレベル記述開始

  
-- ゲートレベル記述終了
end gate_level;
  
