module alwaysRender() {
  if ($preview) {
    render()
    children();
  } else {
    children();
  }
}