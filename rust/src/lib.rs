use std::os::raw::{c_char, c_int};
use std::ffi::CStr;

#[no_mangle]
pub extern "C" fn hello(who: *const c_char) -> c_int {
    let who = unsafe { CStr::from_ptr(who) }.to_string_lossy();
    println!("Hello {} from Rust!", who);
    42
}
