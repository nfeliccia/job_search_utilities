const newProto = navigator.__proto__;
delete newProto.webdriver;  // to simulate a non-automated environment
navigator.__proto__ = newProto;

Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5],
});
Object.defineProperty(navigator, 'languages', {
    get: () => ['en-US', 'en'],
});
// Additional modifications can be added here