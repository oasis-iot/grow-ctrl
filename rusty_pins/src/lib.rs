//Other people's hard work
use pyo3::prelude::*;
use rppal::gpio::Gpio;
use rppal::gpio::OutputPin;

// A Python-ready GPIO output class
#[pyclass(unsendable)]
struct GpioOut{out: OutputPin}

// Behavior of the GPIO output class
#[pymethods]
impl GpioOut { 
    #[new]
    fn new(pin: u8) -> Self { //this is like __init__()
        let io_pin = Gpio::new().unwrap().get(pin).unwrap().into_output();
        GpioOut{out: io_pin}
    }
    
    fn set_high(&mut self){
        self.out.set_high();
    }

    fn set_low(&mut self){
        self.out.set_low();
    }

}

//fn is_active(&self){
//    self.buttn.value();
//}

//fn await_signal(&mut self){
//    self.buttn.wait_for_press(None);
//}

#[pymodule]
fn rusty_pins(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<GpioOut>()?;
    Ok(())
}