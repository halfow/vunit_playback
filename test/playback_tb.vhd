library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

library vunit_lib;
context vunit_lib.vunit_context;

entity playback_tb is
  generic (
      csv : string;
      runner_cfg : string
    );
end entity;

architecture tb of playback_tb is
  -- Clock(s)
  signal clk : std_logic := '0';
  
  -- Wires
  signal data_out : std_logic_vector(7 downto 0) := (others => '0');
  
  -- Stimuli
  signal done : boolean := false;
  constant DATA : integer_array_t := load_csv(csv);
begin

  -- Clock
  clk <= not clk after 5 ns;

  test_runner : process
  begin
    test_runner_setup(runner, runner_cfg);
    wait until done;
    wait until rising_edge(clk);
    test_runner_cleanup(runner);
  end process;

  stimuli_p: process
  begin
    wait until rising_edge(clk);

    info("Stimuli Playback Start");
    for y in 0 to height(DATA)-1 loop
      for x in 0 to width(DATA)-1 loop
        data_out <= std_logic_vector(to_signed(get(DATA, x, y), data_out'length));
        wait until rising_edge(clk);
        -- NOTE: Roll over might occur due to trunkation
        check_equal(signed(data_out), get(DATA, x, y), "Input data is out of range");
      end loop;
    end loop;
    
    info("Stimuli Playback Done");
    data_out <= (others => '0');
    done <= true;
    wait;
  end process stimuli_p;
end architecture;